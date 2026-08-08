## ERPNext - DATEV Integration

Integration between [ERPNext](https://github.com/frappe/erpnext) and DATEV.

- [DATEV Unternehmen Online](https://www.datev.de/web/de/mydatev/online-anwendungen/datev-unternehmen-online/)

    When a voucher is submitted, it will be sent to DATEV Unternehmen Online by email. Either by converting the document to PDF first (outgoing vouchers) or by sending files attached to the document (incoming vouchers).

- DATEV CSV Export

    Export raw **GL Entries** from ERPNext in the DATEV CSV format.

## Install on Frappe Cloud

1. Go to https://frappecloud.com/dashboard/#/sites and click the "New Site" button.
2. In Step 2 ("Select apps to install"), select "ERPNext" and "DATEV Unternehmen Online Integration".
3. Complete the new site wizard.


## Setup DATEV CSV Export

1. DATEV Settings

    Configure you client number, you tax consultant's number and a temporary against account. We recommend keeping the default against account "9090" as described in the [DATEV Help Center](https://apps.datev.de/help-center/documents/1002764).

2. DATEV Report

    Now you can use the report "DATEV". This is a preview of the transactions data. It can be exported, along with the master data, as zip file via the report's menu. Your tax xonsultant can then import your GL Entries into his DATEV system.

3. Generic Settings and Remarks

    The "Remarks" field in Sales and Purchase Invoices is used for the column "Buchungstext". We recommend to use this for a short description of the contents of the invoice. If left blank, ERPNext populates this field with a generic text, that will say nothing about the invoice itself. The field length is limited in the DATEV Export to 60 characters.
    The DATEV Export will contain the sales invoice due date by default. This may raise an OPOS Error during the import. The export can be opted-out in the DATEV Settings.
    OPOS (Offene Posten) is not supported by this app.

> [!IMPORTANT]
> ERPNext does not have automatic VAT deduction ("Automatikkonten") on the GL Entry level. By using the default against account "9090", the automation is disabled.
> 
> If you use a different against account, please ensure to only book to non-automatic accounts in ERPNext. Otherwise, the VAT deduction will be incorrect.

## Setup DATEV Unternehmen Online [en]

1. Open **DATEV Unternehmen Online Settings**
2. Enable the integration
3. Select the _Email Account_ that should be used to send receipts to DATEV Unternehmen Online
4. Add a row to the table
5. Select the _Voucher Type_ (**Sales Invoice**, **Purchase Invoice** or **Expense Claim**)
6. Paste the target email address provided by DATEV Unternehmen Online ([DATEV Help Center](https://apps.datev.de/help-center/documents/1007550))
8. Enable "Add Attachments" or "Add Print"
9. Save

![datev-unternehmen-online-settings](https://user-images.githubusercontent.com/14891507/155744820-f7eb3aa7-ba36-4a66-aa12-80e75fc467de.png)

## Einrichtung DATEV Unternehmen Online [de]

1. Öffnen Sie **DATEV Unternehmen Online-Einstellungen** (engl. **DATEV Unternehmen Online Settings**)
2. Aktivieren Sie die Integration
3. Wählen Sie das _E-Mail-Konto_ (engl. _Email Account_) aus, das für den Versand von Belegen an DATEV Unternehmen Online verwendet werden soll
4. Fügen Sie der Tabelle eine Zeile hinzu
5. Wählen Sie die _Belegart_ (engl. _Voucher Type_)
6. Fügen Sie die für diese Belegart von DATEV Unternehmen Online bereitgestellte Ziel-E-Mail-Adresse ein (mehr dazu im [DATEV Help Center](https://apps.datev.de/help-center/documents/1007550))
    > **Achtung:** Die E-Mail-Adresse des Senders muss mit dem in Schritt 3 ausgewählten E-Mail-Konto übereinstimmen
8. Aktivieren Sie "Anhänge hinzufügen" oder "Druck hinzufügen".
9. Speichern Sie die **DATEV Unternehmen Online-Einstellungen**

## Kompatibilität mit _PDF on Submit_

Falls Sie [PDF on Submit](https://github.com/alyf-de/erpnext_pdf-on-submit) für dieselbe Belegart verwenden, wählen Sie "Anhänge hinzufügen" statt "Druck hinzufügen". _PDF on Submit_ fügt dann die PDF-Datei als Anhang zum Beleg hinzu und die DATEV-Integration versendet diesen.

## Disclaimer

"DATEV" and "DATEV Unternehmen Online" are trademarks of [DATEV eG](https://www.datev.de/). This integration is not approved or endorsed by DATEV eG.

## License

GPLv3
