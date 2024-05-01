# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This is Lino's standard plugin for General Ledger.
See :doc:`/plugins/ledger`.

.. autosummary::
    :toctree:

    fields
    management.commands.reregister

"""

from django.utils.functional import lazystr

from lino.api import ad, _

UPLOADTYPE_SOURCE_DOCUMENT = 1
"""Primary key of upload type "source document" created in :fixture:`std` fixture."""


class Plugin(ad.Plugin):

    verbose_name = _("Accounting")
    needs_plugins = [
        'lino.modlib.weasyprint', 'lino_xl.lib.xl', 'lino.modlib.uploads'
    ]

    ref_length = 4  # 20

    currency_symbol = "€"
    use_pcmn = False
    project_model = None
    worker_model = None

    # intrusive_menu = False
    # """
    # Whether the plugin should integrate into the application's
    # main menu in an intrusive way.  Intrusive means that the main
    # menu gets one top-level item per journal group.
    #
    # The default behaviour is `False`, meaning that these items are
    # gathered below a single item "Accounting".
    # """
    #
    start_year = 2012
    fix_y2k = False
    suppress_movements_until = None

    # Available sales methods:
    SALES_METHODS = {
        'direct': "just invoices",
        'delivery': "delivery notes and invoices",
        'pos': "point of sales",
    }

    sales_method = 'direct'
    has_payment_methods = False
    has_purchases = False

    # sales_stories_journal = "SLS"

    # purchase_stories = True
    # """Whether demo fixture should generate purchase invoices."""

    # registered_states = "registered signed"
    # """The voucher states to be considered as registered.
    #
    # This is specified as a string with a space-separated list of state names,
    # and during startup it is resolved into a tuple of instances of
    # VoucherState.
    #
    # """

    def pre_site_startup(self, site):
        # if isinstance(self.registered_states, str):
        #     s = {
        #         site.models.ledger.VoucherStates.get_by_name(i)
        #             for i in self.registered_states.split()}
        #     self.registered_states = tuple(s)
        if self.sales_method is not None:
            if self.sales_method not in self.SALES_METHODS:
                raise Exception(
                    "Invalid value {} for ledger.sales_method!".format(
                        self.sales_method))
            if self.sales_method == 'pos' and not self.has_payment_methods:
                raise Exception(
                    "When sales_method is 'pos', has_payment_methods must be True."
                )
        super(Plugin, self).pre_site_startup(site)

    def post_site_startup(self, site):
        super(Plugin, self).post_site_startup(site)
        site.models.ledger.CommonAccounts.sort()
        site.models.ledger.VoucherTypes.sort()
        if self.worker_model is not None:
            self.worker_model = site.models.resolve(self.worker_model)

    def setup_main_menu(self, site, user_type, m):
        """
        Add a menu item for every journal.

        Menu items are grouped by journal group. See :class:`lino_xl.lib.ledger.JournalGroups`

        """
        Journal = site.models.ledger.Journal
        JournalGroups = site.models.ledger.JournalGroups
        lp = site.plugins.ledger
        for grp in JournalGroups.get_list_items():
            mg = grp.menu_group
            if mg is None:
                lm = m.add_menu(lp.app_label, lp.verbose_name)
                subm = lm.add_menu(grp.name, grp.text)
            else:
                subm = m.add_menu(mg.app_label, mg.verbose_name)
            for jnl in Journal.objects.filter(
                    journal_group=grp).order_by('seqno'):
                subm.add_action(jnl.voucher_type.table_class,
                                label=lazystr(jnl),
                                params=dict(master_instance=jnl))
        lm = m.add_menu(lp.app_label, lp.verbose_name)
        lm.add_action('ledger.MyMovements')

    def setup_reports_menu(self, site, user_type, m):
        if site.is_installed("finan"):
            mg = site.plugins.ledger
            m = m.add_menu(mg.app_label, mg.verbose_name)
            # m.add_action('ledger.Situation')
            # m.add_action('ledger.ActivityReport')
            # m.add_action('ledger.AccountingReport')
            # m.add_action('ledger.GeneralAccountBalances')
            # m.add_action('ledger.CustomerAccountBalances')
            # m.add_action('ledger.SupplierAccountBalances')
            m.add_action('ledger.Debtors')
            m.add_action('ledger.Creditors')

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.ledger
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Accounts')
        m.add_action('ledger.Journals')
        m.add_action('ledger.FiscalYears')
        m.add_action('ledger.AccountingPeriods')
        m.add_action('ledger.PaymentTerms')
        if self.has_payment_methods:
            m.add_action('ledger.PaymentMethods')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.ledger
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.CommonAccounts')
        m.add_action('ledger.MatchRules')
        m.add_action('ledger.AllVouchers')
        m.add_action('ledger.VoucherTypes')
        m.add_action('ledger.AllMovements')
        m.add_action('ledger.TradeTypes')
        m.add_action('ledger.JournalGroups')

    def remove_dummy(self, *args):
        lst = list(args)
        if self.project_model is None:
            lst.remove('project')
        return lst

    def get_dashboard_items(self, user):
        yield self.site.models.ledger.MyMovements
        yield self.site.models.ledger.JournalsOverview
