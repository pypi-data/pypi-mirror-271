#! /usr/bin/python3
"""
Testbed for managing transactions in
SAP using the service layer
"""
import requests
import urllib3

from copy import deepcopy


class Service:
    api_server = None
    api_port = None
    api_url = None

    api_username = None
    api_password = None
    api_company = None

    api_session = None

    entities = {
        'AccountCategory': 'AccountCategory',
        'AccountSegmentationCategories': 'AccountSegmentationCategories',
        'AccountSegmentations': 'AccountSegmentations',
        'AccrualTypes': 'AccrualTypes',
        'Activities': 'Activities',
        'ActivityLocations': 'ActivityLocations',
        'ActivityRecipientLists': 'ActivityRecipientLists',
        'ActivityStatuses': 'ActivityStatuses',
        'ActivityTypes': 'ActivityTypes',
        'AdditionalExpenses': 'AdditionalExpenses',
        'AlertManagements': 'AlertManagements',
        'AlternateCatNum': 'AlternateCatNum',
        'ApprovalRequests': 'ApprovalRequests',
        'ApprovalStages': 'ApprovalStages',
        'ApprovalTemplates': 'ApprovalTemplates',
        'AssetCapitalization': 'AssetCapitalization',
        'AssetCapitalizationCreditMemo': 'AssetCapitalizationCreditMemo',
        'AssetClasses': 'AssetClasses',
        'AssetDepreciationGroups': 'AssetDepreciationGroups',
        'AssetGroups': 'AssetGroups',
        'AssetManualDepreciation': 'AssetManualDepreciation',
        'AssetRetirement': 'AssetRetirement',
        'AssetTransfer': 'AssetTransfer',
        'Attachments2': 'Attachments2',
        'AttributeGroups': 'AttributeGroups',
        'B1Sessions': 'B1Sessions',
        'BankChargesAllocationCodes': 'BankChargesAllocationCodes',
        'BankPages': 'BankPages',
        'Banks': 'Banks',
        'BankStatements': 'BankStatements',
        'BarCodes': 'BarCodes',
        'BatchNumberDetails': 'BatchNumberDetails',
        'BillOfExchangeTransactions': 'BillOfExchangeTransactions',
        'BinLocationAttributes': 'BinLocationAttributes',
        'BinLocationFields': 'BinLocationFields',
        'bins': 'BinLocations',
        'BlanketAgreements': 'BlanketAgreements',
        'BOEDocumentTypes': 'BOEDocumentTypes',
        'BOEInstructions': 'BOEInstructions',
        'BOEPortfolios': 'BOEPortfolios',
        'BPFiscalRegistryID': 'BPFiscalRegistryID',
        'BPPriorities': 'BPPriorities',
        'Branches': 'Branches',
        'BrazilBeverageIndexers': 'BrazilBeverageIndexers',
        'BrazilFuelIndexers': 'BrazilFuelIndexers',
        'BrazilMultiIndexers': 'BrazilMultiIndexers',
        'BrazilNumericIndexers': 'BrazilNumericIndexers',
        'BrazilStringIndexers': 'BrazilStringIndexers',
        'BudgetDistributions': 'BudgetDistributions',
        'Budgets': 'Budgets',
        'BudgetScenarios': 'BudgetScenarios',
        'BusinessPartnerGroups': 'BusinessPartnerGroups',
        'BusinessPartnerProperties': 'BusinessPartnerProperties',
        'BusinessPartners': 'BusinessPartners',
        'BusinessPlaces': 'BusinessPlaces',
        'CampaignResponseType': 'CampaignResponseType',
        'Campaigns': 'Campaigns',
        'CashDiscounts': 'CashDiscounts',
        'CashFlowLineItems': 'CashFlowLineItems',
        'CertificateSeries': 'CertificateSeries',
        'ChartOfAccounts': 'ChartOfAccounts',
        'ChecksforPayment': 'ChecksforPayment',
        'ChooseFromList': 'ChooseFromList',
        'ClosingDateProcedure': 'ClosingDateProcedure',
        'Cockpits': 'Cockpits',
        'CommissionGroups': 'CommissionGroups',
        'Contacts': 'Contacts',
        'ContractTemplates': 'ContractTemplates',
        'CorrectionInvoice': 'CorrectionInvoice',
        'CorrectionInvoiceReversal': 'CorrectionInvoiceReversal',
        'CorrectionPurchaseInvoice': 'CorrectionPurchaseInvoice',
        'CorrectionPurchaseInvoiceReversal': 'CorrectionPurchaseInvoiceReversal',
        'CostCenterTypes': 'CostCenterTypes',
        'CostElements': 'CostElements',
        'Countries': 'Countries',
        'CreditCardPayments': 'CreditCardPayments',
        'CreditCards': 'CreditCards',
        'credit notes': 'CreditNotes',
        'CreditPaymentMethods': 'CreditPaymentMethods',
        'Currencies': 'Currencies',
        'CustomerEquipmentCards': 'CustomerEquipmentCards',
        'CustomsDeclaration': 'CustomsDeclaration',
        'CustomsGroups': 'CustomsGroups',
        'CycleCountDeterminations': 'CycleCountDeterminations',
        'DeductionTaxGroups': 'DeductionTaxGroups',
        'DeductionTaxHierarchies': 'DeductionTaxHierarchies',
        'DeductionTaxSubGroups': 'DeductionTaxSubGroups',
        'deliveries': 'DeliveryNotes',
        'Departments': 'Departments',
        'Deposits': 'Deposits',
        'DepreciationAreas': 'DepreciationAreas',
        'DepreciationTypePools': 'DepreciationTypePools',
        'DepreciationTypes': 'DepreciationTypes',
        'DeterminationCriterias': 'DeterminationCriterias',
        'Dimensions': 'Dimensions',
        'DistributionRules': 'DistributionRules',
        'DNFCodeSetup': 'DNFCodeSetup',
        'DownPayments': 'DownPayments',
        'Drafts': 'Drafts',
        'DunningLetters': 'DunningLetters',
        'DunningTerms': 'DunningTerms',
        'DynamicSystemStrings': 'DynamicSystemStrings',
        'ElectronicFileFormats': 'ElectronicFileFormats',
        'EmailGroups': 'EmailGroups',
        'EmployeeIDType': 'EmployeeIDType',
        'EmployeePosition': 'EmployeePosition',
        'EmployeeRolesSetup': 'EmployeeRolesSetup',
        'EmployeesInfo': 'EmployeesInfo',
        'EmployeeStatus': 'EmployeeStatus',
        'EmployeeTransfers': 'EmployeeTransfers',
        'EmploymentCategorys': 'EmploymentCategorys',
        'EnhancedDiscountGroups': 'EnhancedDiscountGroups',
        'ExceptionalEvents': 'ExceptionalEvents',
        'ExtendedTranslations': 'ExtendedTranslations',
        'FAAccountDeterminations': 'FAAccountDeterminations',
        'FactoringIndicators': 'FactoringIndicators',
        'FinancialYears': 'FinancialYears',
        'FiscalPrinter': 'FiscalPrinter',
        'FormattedSearches': 'FormattedSearches',
        'FormPreferences': 'FormPreferences',
        'Forms1099': 'Forms1099',
        'GLAccountAdvancedRules': 'GLAccountAdvancedRules',
        'GoodsReturnRequest': 'GoodsReturnRequest',
        'GovPayCodes': 'GovPayCodes',
        'Holidays': 'Holidays',
        'HouseBankAccounts': 'HouseBankAccounts',
        'IncomingPayments': 'IncomingPayments',
        'Industries': 'Industries',
        'IntegrationPackagesConfigure': 'IntegrationPackagesConfigure',
        'InternalReconciliations': 'InternalReconciliations',
        'IntrastatConfiguration': 'IntrastatConfiguration',
        'InventoryCountings': 'InventoryCountings',
        'InventoryCycles': 'InventoryCycles',
        'InventoryGenEntries': 'InventoryGenEntries',
        'InventoryGenExits': 'InventoryGenExits',
        'InventoryOpeningBalances': 'InventoryOpeningBalances',
        'InventoryPostings': 'InventoryPostings',
        'InventoryTransferRequests': 'InventoryTransferRequests',
        'invoices': 'Invoices',
        'item groups': 'ItemGroups',
        'ItemImages': 'ItemImages',
        'ItemProperties': 'ItemProperties',
        'items': 'Items',
        'JournalEntries': 'JournalEntries',
        'JournalEntryDocumentTypes': 'JournalEntryDocumentTypes',
        'KnowledgeBaseSolutions': 'KnowledgeBaseSolutions',
        'KPIs': 'KPIs',
        'LandedCosts': 'LandedCosts',
        'LandedCostsCodes': 'LandedCostsCodes',
        'LegalData': 'LegalData',
        'LengthMeasures': 'LengthMeasures',
        'LocalEra': 'LocalEra',
        'Manufacturers': 'Manufacturers',
        'MaterialGroups': 'MaterialGroups',
        'MaterialRevaluation': 'MaterialRevaluation',
        'Messages': 'Messages',
        'MobileAddOnSetting': 'MobileAddOnSetting',
        'MultiLanguageTranslations': 'MultiLanguageTranslations',
        'NatureOfAssessees': 'NatureOfAssessees',
        'NCMCodesSetup': 'NCMCodesSetup',
        'NFModels': 'NFModels',
        'NFTaxCategories': 'NFTaxCategories',
        'NotaFiscalCFOP': 'NotaFiscalCFOP',
        'NotaFiscalCST': 'NotaFiscalCST',
        'NotaFiscalUsage': 'NotaFiscalUsage',
        'OccurrenceCodes': 'OccurrenceCodes',
        'sales orders': 'Orders',
        'PackagesTypes': 'PackagesTypes',
        'PartnersSetups': 'PartnersSetups',
        'PaymentBlocks': 'PaymentBlocks',
        'PaymentDrafts': 'PaymentDrafts',
        'PaymentReasonCodes': 'PaymentReasonCodes',
        'PaymentRunExport': 'PaymentRunExport',
        'PaymentTermsTypes': 'PaymentTermsTypes',
        'PickLists': 'PickLists',
        'POSDailySummary': 'POSDailySummary',
        'PredefinedTexts': 'PredefinedTexts',
        'PriceLists': 'PriceLists',
        'ProductionOrders': 'ProductionOrders',
        'ProductTrees': 'ProductTrees',
        'ProfitCenters': 'ProfitCenters',
        'ProjectManagements': 'ProjectManagements',
        'ProjectManagementTimeSheet': 'ProjectManagementTimeSheet',
        'Projects': 'Projects',
        'purchase credits': 'PurchaseCreditNotes',
        'receipt of goods': 'PurchaseDeliveryNotes',
        'payable down payments': 'PurchaseDownPayments',
        'payable invoices': 'PurchaseInvoices',
        'purchase orders': 'PurchaseOrders',
        'purchase quotes': 'PurchaseQuotations',
        'purchase requests': 'PurchaseRequests',
        'purchase returns': 'PurchaseReturns',
        'payable tax invoices': 'PurchaseTaxInvoices',
        'QueryAuthGroups': 'QueryAuthGroups',
        'QueryCategories': 'QueryCategories',
        'Queue': 'Queue',
        'Quotations': 'Quotations',
        'Relationships': 'Relationships',
        'ReportFilter': 'ReportFilter',
        'ReportTypes': 'ReportTypes',
        'ResourceCapacities': 'ResourceCapacities',
        'ResourceGroups': 'ResourceGroups',
        'ResourceProperties': 'ResourceProperties',
        'Resources': 'Resources',
        'RetornoCodes': 'RetornoCodes',
        'ReturnRequest': 'ReturnRequest',
        'delivery returns': 'Returns',
        'RouteStages': 'RouteStages',
        'SalesForecast': 'SalesForecast',
        'SalesOpportunities': 'SalesOpportunities',
        'SalesOpportunityCompetitorsSetup': 'SalesOpportunityCompetitorsSetup',
        'SalesOpportunityInterestsSetup': 'SalesOpportunityInterestsSetup',
        'SalesOpportunityReasonsSetup': 'SalesOpportunityReasonsSetup',
        'SalesOpportunitySourcesSetup': 'SalesOpportunitySourcesSetup',
        'SalesPersons': 'SalesPersons',
        'SalesStages': 'SalesStages',
        'SalesTaxAuthorities': 'SalesTaxAuthorities',
        'SalesTaxAuthoritiesTypes': 'SalesTaxAuthoritiesTypes',
        'SalesTaxCodes': 'SalesTaxCodes',
        'SalesTaxInvoices': 'SalesTaxInvoices',
        'Sections': 'Sections',
        'SerialNumberDetails': 'SerialNumberDetails',
        'ServiceCallOrigins': 'ServiceCallOrigins',
        'ServiceCallProblemSubTypes': 'ServiceCallProblemSubTypes',
        'ServiceCallProblemTypes': 'ServiceCallProblemTypes',
        'ServiceCalls': 'ServiceCalls',
        'ServiceCallSolutionStatus': 'ServiceCallSolutionStatus',
        'ServiceCallStatus': 'ServiceCallStatus',
        'ServiceCallTypes': 'ServiceCallTypes',
        'ServiceContracts': 'ServiceContracts',
        'ServiceGroups': 'ServiceGroups',
        'ShippingTypes': 'ShippingTypes',
        'SpecialPrices': 'SpecialPrices',
        'States': 'States',
        'StockTakings': 'StockTakings',
        'StockTransferDrafts': 'StockTransferDrafts',
        'transfers': 'StockTransfers',
        'TargetGroups': 'TargetGroups',
        'TaxCodeDeterminations': 'TaxCodeDeterminations',
        'TaxCodeDeterminationsTCD': 'TaxCodeDeterminationsTCD',
        'TaxInvoiceReport': 'TaxInvoiceReport',
        'TaxWebSites': 'TaxWebSites',
        'Teams': 'Teams',
        'TerminationReason': 'TerminationReason',
        'Territories': 'Territories',
        'TrackingNotes': 'TrackingNotes',
        'TransactionCodes': 'TransactionCodes',
        'TransportationDocuments': 'TransportationDocuments',
        'UnitOfMeasurementGroups': 'UnitOfMeasurementGroups',
        'UnitOfMeasurements': 'UnitOfMeasurements',
        'UserDefaultGroups': 'UserDefaultGroups',
        'UserFieldsMD': 'UserFieldsMD',
        'UserKeysMD': 'UserKeysMD',
        'UserLanguages': 'UserLanguages',
        'UserObjectsMD': 'UserObjectsMD',
        'UserPermissionTree': 'UserPermissionTree',
        'UserQueries': 'UserQueries',
        'Users': 'Users',
        'UserTablesMD': 'UserTablesMD',
        'ValueMapping': 'ValueMapping',
        'ValueMappingCommunication': 'ValueMappingCommunication',
        'VatGroups': 'VatGroups',
        'VendorPayments': 'VendorPayments',
        'WarehouseLocations': 'WarehouseLocations',
        'Warehouses': 'Warehouses',
        'bin sublevels': 'WarehouseSublevelCodes',
        'WebClientBookmarkTiles': 'WebClientBookmarkTiles',
        'WebClientDashboards': 'WebClientDashboards',
        'WebClientFormSettings': 'WebClientFormSettings',
        'WebClientLaunchpads': 'WebClientLaunchpads',
        'WebClientListviewFilters': 'WebClientListviewFilters',
        'WebClientNotifications': 'WebClientNotifications',
        'WebClientPreferences': 'WebClientPreferences',
        'WebClientRecentActivities': 'WebClientRecentActivities',
        'WebClientVariantGroups': 'WebClientVariantGroups',
        'WebClientVariants': 'WebClientVariants',
        'WeightMeasures': 'WeightMeasures',
        'WithholdingTaxCodes': 'WithholdingTaxCodes',
        'WitholdingTaxDefinition': 'WitholdingTaxDefinition',
        'WizardPaymentMethods': 'WizardPaymentMethods',
        'WTaxTypeCodes': 'WTaxTypeCodes'
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self,
                 usr: str,
                 pwrd: str,
                 compDB: str,
                 srvr: str,
                 prt: int = 50000):
        self.api_username = usr
        self.api_password = pwrd
        self.api_company = compDB

        self.api_server = srvr
        self.api_port = prt

        self.api_url = '' + \
            f'https://{self.api_server}:' + \
            f'{self.api_port}/b1s/v1/'

    def __str__(self):
        return '' + \
            f'API Server: {self.api_server}\n' + \
            f'API Port: {self.api_port}\n' + \
            f'API_URL: {self.api_url}\n' + \
            f'API User: {self.api_username}\n' + \
            f'API Password: {self.api_password}\n' + \
            f'API Company: {self.api_company}\n' + \
            f'API Session: {self.api_session}\n'

    def entity(self, name: str):
        return self.entities.get(name)

    def login(self):
        self.api_session = requests.Session()

        url = f'{self.api_url}Login'

        payload = {
            'UserName': self.api_username,
            'Password': self.api_password,
            'CompanyDB': self.api_company}

        response = self.api_session.post(url, json=payload, verify=False)

        return response

    def logout(self):
        if self.api_session:
            url = f'{self.api_url}Logout'

            response = self.api_session.post(url, verify=False)

            self.api_session = None
            self.api_server = None
            self.api_port = None
            self.api_url = None
            self.api_username = None
            self.api_password = None
            self.api_company = None

            return response

    def switch_company(self,
                       new_company: str):
        switch = False

        if new_company != self.api_company:
            switch = True

        if not self.api_session:
            switch = True

        if not switch:
            return

        self.api_company = new_company

        self.api_session = requests.Session()

        url = f'{self.api_url}Login'

        payload = {
            'UserName': self.api_username,
            'Password': self.api_password,
            'CompanyDB': self.api_company}

        return self.api_session.post(url, json=payload, verify=False)

    def create_entity(self,
                      type: str,
                      info: dict):
        url = f"{self.api_url}{type}"

        response = self.api_session.post(url, json=info)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']

            return ret_val

        data = response.json()

        ret_val['metadata'] = data.get('odata.metadata')

        values = data.get('value')

        if values:
            for row in values:
                ret_val['data'].append(row)

            ret_val['success'] = True
        elif values == []:
            ret_val['error'] = 404
            ret_val['error_message'] = 'Entity creation failed'
        else:
            ret_val['data'].append(data)

            ret_val['success'] = True

        return ret_val

    def read_entity(self,
                    type: str,
                    id=None,
                    code=None,
                    filter: str = None,
                    next=None,
                    count=False):
        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None
        }

        if count:
            url = f'{self.api_url}{type}/$count'

            ret_val['url'] = url

            response = self.api_session.get(url)

            ret_val['data'] = response.json()

            return ret_val
        elif next:
            url = f'{self.api_url}{next}'
        elif filter:
            url = f'{self.api_url}{type}'
            url += f'?$filter={filter}'
        elif id:
            url = f"{self.api_url}{type}({id})"
        elif code:
            url = f"{self.api_url}{type}('{code}')"
        else:
            url = f"{self.api_url}{type}"

        response = self.api_session.get(url)

        ret_val['code'] = response.status_code
        ret_val['url'] = url

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error
            ret_val['error_message'] = message

            return ret_val

        data = response.json()

        ret_val['metadata'] = data.get('odata.metadata')
        ret_val['next'] = data.get('odata.nextLink')

        values = data.get('value')

        if values:
            for row in values:
                ret_val['data'].append(row)

            ret_val['success'] = True
        elif values == []:
            ret_val['error'] = 404
            ret_val['error_message'] = 'No data found'
        else:
            ret_val['data'].append(data)

            ret_val['success'] = True

        return ret_val

    def update_entity(self,
                      type: str,
                      info: dict,
                      key: str):
        code = info[key]

        if isinstance(code, int):
            url = f"{self.api_url}{type}({code})"
        else:
            url = f"{self.api_url}{type}('{code}')"

        data = deepcopy(info)

        data.pop(key)

        response = self.api_session.patch(url, json=data)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']

            return ret_val

        ret_val['success'] = True

        return ret_val

    def delete_entity(self,
                      type: str,
                      code):
        if isinstance(code, int):
            url = f"{self.api_url}{type}({code})"
        else:
            url = f"{self.api_url}{type}('{code}')"

        response = self.api_session.delete(url)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error
            ret_val['error_message'] = message
        else:
            ret_val['success'] = True

        return ret_val

    def create_document(self,
                        type: str,
                        doc_info: dict,
                        force_log=False):
        url = f"{self.api_url}{type}"

        response = self.api_session.post(url, json=doc_info)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message

            return ret_val

        data = response.json()

        ret_val['metadata'] = data.get('odata.metadata')

        values = data.get('value')

        if values:
            for row in values:
                ret_val['data'].append(row)

            ret_val['success'] = True
        elif values == []:
            ret_val['error'] = 404
            ret_val['error_message'] = 'Document creation failed'
        else:
            ret_val['data'].append(data)

            ret_val['success'] = True

        return ret_val

    def read_documents(self,
                       type: str,
                       docentry: int = None,
                       docnum: int = None,
                       skip=None,
                       filter: str = None,
                       count=False):
        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None
        }

        if count:
            url = f'{self.api_url}{type}/$count'

            ret_val['url'] = url

            response = self.api_session.get(url)

            ret_val['data'] = response.json()

            return ret_val
        elif docentry:
            url = f'{self.api_url}{type}({docentry})'
        elif docnum:
            url = f'{self.api_url}{type}?$filter=DocNum eq {docnum}'
        elif filter:
            url = f'{self.api_url}{type}?$filter={filter}'

            if skip:
                url += f'&$skip={skip}'
        elif skip:
            url = f'{self.api_url}{type}?$skip={skip}'
        else:
            url = f'{self.api_url}{type}'

        response = self.api_session.get(url)

        ret_val['url'] = url
        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error
            ret_val['error_message'] = message

            return ret_val

        data = response.json()

        ret_val['metadata'] = data.get('odata.metadata')
        ret_val['next'] = data.get('odata.nextLink')

        values = data.get('value')

        if values:
            for row in values:
                ret_val['data'].append(row)

            ret_val['success'] = True
        elif values == []:
            ret_val['error'] = 404
            ret_val['error_message'] = 'No data found'
        else:
            ret_val['data'].append(data)

            ret_val['success'] = True

        return ret_val

    def update_document(self,
                        type: str,
                        info: dict,
                        key: str):
        code = info[key]

        url = f"{self.api_url}{type}({code})"

        response = self.api_session.put(url, json=info)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']

            return ret_val

        ret_val['success'] = True

        return ret_val

    def cancel_document(self,
                        type: str,
                        docentry: int = None):
        if not docentry:
            return None

        url = f'{self.api_url}{type}({docentry})/Cancel'

        response = self.api_session.post(url)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']
        else:
            ret_val['success'] = True

        return ret_val

    def close_document(self,
                       type: str,
                       docentry: int = None):
        if not docentry:
            return None

        url = f'{self.api_url}{type}({docentry})/Close'

        response = self.api_session.post(url)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']
        else:
            ret_val['success'] = True

        return ret_val

    def reopen_document(self,
                        type: str,
                        docentry: int = None):
        if not docentry:
            return None

        url = f'{self.api_url}{type}({docentry})/Reopen'

        response = self.api_session.post(url)

        ret_val = {
            'metadata': None,
            'data': [],
            'success': False,
            'error': None,
            'error_message': None,
            'code': None,
            'next': None,
            'url': url
        }

        ret_val['code'] = response.status_code

        if 400 <= response.status_code < 500:
            contents = response.json()

            error = contents['error']
            message = error['message']

            ret_val['error'] = error['code']
            ret_val['error_message'] = message['value']
        else:
            ret_val['success'] = True

        return ret_val

    def create_cancelation_document(self,
                                    type: str,
                                    docentry: int = None):
        if not docentry:
            return None

        url = f'{self.api_url}{type}({docentry})/CreateCancellationDocument'

        response = self.api_session.post(url)

        return response

    def read_UDF(self,
                 type: str,
                 code=None,
                 filter: str = None):
        if code:
            url = f'{type}(\'{code}\')'
        elif filter:
            url = f'{type}?$filter={filter}'
        else:
            return

        return self.read_entity('', next=url)

    def create_UDO(self,
                   type: str,
                   info: dict):
        return self.create_document(type, info)

    def read_UDO(self,
                 type: str,
                 code=None,
                 filter: str = None):
        return self.read_documents(type, docentry=code, filter=filter)
