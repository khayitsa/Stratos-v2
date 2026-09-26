import os
from datetime import datetime
from pathlib import Path
from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "stratos-local-development-key"

# ---------------------------------------------------------------------------
# COMPANY / LEGAL DETAILS SHOWN IN THE FOOTER
# These were "[EXACT LEGAL NAME]" and "[LICENCE NUMBER]" placeholders. They must
# come from Palesa / Miguel (marketing + legal group) - do NOT invent them.
# Set them here, or as environment variables on PythonAnywhere:
#   STRATOS_LEGAL_NAME, STRATOS_LICENCE_NO, STRATOS_DISCLAIMER
# While they are empty the footer simply omits those sentences (no brackets).
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ARTICLES ARE PRIVATE until legal has approved them.
# While False: no "Articles" link in the menu/footer and /articles + /articles/<slug>/ return 404.
# To publish later: set ARTICLES_PUBLIC = True here (or set the env var STRATOS_ARTICLES_PUBLIC=1).
# To preview privately meanwhile: set STRATOS_ARTICLES_PREVIEW_KEY=<secret> and open /articles?preview=<secret>
# (that unlocks the pages for your browser session only).
# ---------------------------------------------------------------------------
ARTICLES_PUBLIC = os.environ.get("STRATOS_ARTICLES_PUBLIC", "") == "1"
ARTICLES_PREVIEW_KEY = os.environ.get("STRATOS_ARTICLES_PREVIEW_KEY", "")

COMPANY = {
    "email": "info@stratosuae.com",
    # Office address: replace with the exact wording on the Canva letterhead (one string per line).
    "address_lines": ["Nad Al Sheba 1", "Dubai, United Arab Emirates"],
    "legal_name": os.environ.get("STRATOS_LEGAL_NAME", ""),
    "licence_no": os.environ.get("STRATOS_LICENCE_NO", ""),
    "licence_authority": "Meydan Free Zone",
    "disclaimer": os.environ.get("STRATOS_DISCLAIMER", ""),
}


@app.context_processor
def inject_globals():
    return {"company": COMPANY, "current_year": datetime.now().year,
            "articles_public": articles_visible(), "service_icons": SERVICE_ICONS}


def articles_visible():
    """True when the Articles pages may be shown to this visitor."""
    if ARTICLES_PUBLIC:
        return True
    return bool(ARTICLES_PREVIEW_KEY) and session.get("articles_preview") is True


# Brand-kit icons (already in /images/icons) used for each service
SERVICE_ICONS = {
    "complete_uae_establishment": "remote-coordination_icon.svg",
    "uae_company_formation": "business-formation_icon.svg",
    "accounting_management_reporting": "accounting-and-bookkeeping_icon.svg",
    "business_bank_account_support": "bank-account-opening_icon.svg",
    "residence_visa_support": "residency-and-visas_icon.svg",
    "corporate_administration_governance": "single-point-of-accountability_icon.svg",
    "corporate_tax_vat_coordination": "auditing_icon.svg",
}


USERS = {
    "client": {"password": "stratos2026", "role": "client", "display_name": "Client"},
    "admin": {"password": "stratos2026", "role": "admin", "display_name": "Admin"},
}


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/logo")
def logo():
    return send_from_directory(BASE_DIR, "STRATOS Primary Logo.svg.svg")


@app.get("/images/<path:filename>")
def image_asset(filename):
    return send_from_directory(BASE_DIR / "images", filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        selected_role = request.form.get("role", "client")
        user = USERS.get(username)
        if user and user["password"] == password and user["role"] == selected_role:
            session["username"] = username
            session["role"] = user["role"]
            session["display_name"] = user["display_name"]
            return redirect(url_for("client_dashboard" if user["role"] == "client" else "admin_dashboard"))
        error = "The portal, username, or password does not match."
    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/client/")
def client_dashboard():
    if session.get("role") != "client":
        return redirect(url_for("login"))
    return render_template("client/dashboard.html")


@app.get("/admin/")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin/dashboard.html")


@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/services")
def services():
    # Services overview merged into the home page (26 Sep review): the home page already lists every service.
    return redirect(url_for("home") + "#services")


SERVICE_PAGES = {
    "complete_uae_establishment": {
        "path": "/services/complete-uae-establishment/",
        "title": "Complete UAE Business Establishment | Stratos Consulting",
        "meta_description": "Advisory-led UAE establishment covering structure comparison, company formation, banking preparation, residence, bookkeeping and ongoing support.",
        "label": "FLAGSHIP ENGAGEMENT",
        "heading": "Complete UAE Establishment, from Structure to Operation.",
        "intro": "A managed engagement for international founders and groups that need the UAE company to work commercially, fit within a wider ownership structure and be ready for banking, residence and ongoing corporate requirements.",
        "secondary": "See What the Engagement Covers",
        "sections": [
            {"heading": "More Than a Licence Application.", "paragraphs": [
                "A company can be incorporated correctly and still be poorly suited to the business.",
                "The licence may not reflect the actual activities. The jurisdiction may create unnecessary operating restrictions. The ownership documents may be difficult to explain to a bank. Visa capacity, premises, tax registration and bookkeeping may only be considered after deadlines begin to run.",
                "Complete UAE Establishment addresses those dependencies before they become separate problems.",
                "We establish the commercial facts, compare suitable routes, document the recommendation and coordinate the agreed implementation in the appropriate sequence."
            ]},
            {"heading": "Complete UAE Establishment is suited to:", "items": [
                "International groups adding a UAE holding or operating company.", "Family offices and private investment groups requiring a clearly documented UAE entity.", "Founders with shareholders, customers, suppliers or operations in several countries.", "Established businesses entering the UAE market.", "Trading, commodities, distribution, technology, consulting, property, hospitality, manufacturing and logistics businesses with material operating requirements.", "Clients expecting to require banking, residence, bookkeeping and continuing corporate support after formation."
            ], "note": "It is not designed as a low-cost licence or visa procurement service."},
            {"heading": "What You Receive Before Formation", "cards": [
                ["Business & Ownership Assessment", "We review the proposed activities, ownership, existing group entities, target markets, counterparties, staffing, premises, residence requirements, banking profile and expected transaction flows."],
                ["Written Mainland & Free-Zone Comparison", "We compare appropriate routes against the facts of the business, including permitted activities, operating reach, ownership, licence requirements, workspace, visa implications, establishment costs, recurring administration and material banking considerations. The objective is to narrow the options, not produce a catalogue."],
                ["Commercial Recommendation", "We provide a reasoned recommendation setting out the proposed route, the basis for it, material assumptions and principal trade-offs."],
                ["Implementation Scope", "You receive a defined proposal identifying the agreed services, sequence, responsibilities, professional fees, anticipated government or third-party charges, assumptions and exclusions."]
            ]},
            {"heading": "What We Can Coordinate After the Recommendation", "cards": [
                ["Company Formation", "Trade-name, activity, legal-form and application coordination for the agreed mainland or free-zone company."], ["Banking Preparation", "Potential bank-fit assessment, business-profile drafting, KYC and supporting-document preparation and application support."], ["Residence & Immigration", "Coordination of eligible owner, employee and dependant applications and connected procedural steps."], ["Bookkeeping Set-Up", "Chart-of-accounts design, bookkeeping process, opening records, reporting timetable and information collection."], ["Tax Readiness", "Preparation of financial information and coordination with appropriately qualified tax professionals where formal assessment, registration or filing is required."], ["Corporate Administration", "Renewal planning, company records, governance actions, amendments and recurring administrative requirements included in the agreed scope."]
            ], "note": "Not every business requires every workstream. We recommend the work relevant to the company rather than adding services to fill a package."},
            {"heading": "The Establishment Process", "steps": [
                ["Qualification", "You provide initial information about the business, owners, expected timing, banking, visas and ongoing requirements."], ["Discovery", "We collect and review the commercial, ownership and acceptance information required to understand the proposed UAE operation."], ["Comparison & Recommendation", "We assess appropriate mainland and free-zone routes and issue the written comparison and commercial recommendation."], ["Formation & Set-Up", "Once the route and scope are approved, we coordinate the agreed formation and connected operational workstreams."], ["Handover or Continued Support", "We confirm what has been completed, what remains outstanding and which obligations continue. Stratos can remain responsible for agreed bookkeeping, administration, immigration and specialist coordination."]
            ]},
            {"heading": "Decisions We Do Not Pretend to Control", "paragraphs": ["A bank decides whether to open or maintain an account. A licensing authority decides whether to approve an activity or application. Immigration and tax authorities apply their own rules and review processes.", "We improve readiness, present the business accurately and manage the process carefully. We do not guarantee approval, fixed processing times or treatment by an independent institution."]}
        ],
        "faq": [["How do you decide between a mainland and free-zone company?", "We compare the routes against the activities, customer and supplier markets, ownership, premises, staffing, visas, banking profile and longer-term plans. There is no universally superior route."], ["What is included in the written recommendation?", "The recommendation ordinarily identifies the relevant routes, compares their material implications, states the recommended structure and records the main reasons, assumptions and trade-offs."], ["How long does a complete UAE establishment take?", "Timing depends on the activity, jurisdiction, ownership, document readiness, external approvals, immigration requirements and bank review."], ["How much does the engagement cost?", "The cost depends on the structure, ownership, number of workstreams and specialist involvement. The proposal separates Stratos fees from government and third-party costs."], ["Can you guarantee a UAE bank account?", "No. Banks make their own decisions."], ["Can you work with our existing lawyers, tax advisers or family-office team?", "Yes. We can coordinate with existing advisers and agree responsibilities rather than replacing functioning professional relationships."]],
        "cta_label": "BEGIN WITH THE STRUCTURE", "cta_heading": "Establish the UAE Business as Part of the Bigger Picture.", "cta_copy": "Submit the ownership, activities, markets, banking requirements, visas and intended timing. If the engagement appears suitable, we will invite you to a consultation."
    },
    "uae_company_formation": {
        "path": "/services/uae-company-formation/", "title": "UAE Mainland & Free Zone Company Formation | Stratos", "meta_description": "UAE mainland and free-zone company formation with activity assessment, document preparation, licensing and incorporation coordination.", "label": "COMPANY FORMATION", "heading": "UAE Company Formation with the Operating Requirements Already Considered.", "intro": "Mainland and free-zone company formation for businesses that want the licence, ownership, banking profile and post-incorporation requirements to point in the same direction.", "secondary": "Compare Our Establishment Services", "sections": [
            {"heading": "Formation Is Implementation, Not Guesswork.", "paragraphs": ["The formation process should begin once the business requirements and proposed route are understood.", "We confirm the agreed activity, jurisdiction, legal form, ownership and implementation requirements before preparing the application.", "If those decisions have not yet been properly assessed, we will recommend beginning with Complete UAE Establishment rather than pushing an uncertain structure into formation."]},
            {"heading": "Mainland Company Formation", "paragraphs": ["A mainland company may be appropriate where the intended activities, customers, physical operations, premises or government relationships favour a mainland structure.", "We assess the specific business rather than making broad claims that mainland is always more flexible or more credible.", "The scope can include activity and legal-form confirmation, document requirements, trade-name and initial-approval coordination, licensing steps and agreed post-licence actions."]},
            {"heading": "Free-Zone Company Formation", "paragraphs": ["A free-zone company may be appropriate where the selected zone, available activities, ownership requirements, workspace, visas, operating model and cost structure align with the business.", "Free zone does not describe one standard product. Authorities differ in activities, documentation, facilities, processes and recurring requirements.", "We compare only the free-zone options relevant to the business rather than directing every applicant to the same package."]},
            {"heading": "Formation Scope", "cards": [["Pre-Application Confirmation", "Confirmation of the agreed jurisdiction, licence activities, legal form, ownership, applicant documentation and known external approvals."], ["Document Preparation", "A clear document checklist and coordination of shareholder, beneficial-owner, corporate and supporting information."], ["Application Coordination", "Preparation and submission support for agreed authority applications and management of routine queries and status follow-up."], ["Licensing & Incorporation", "Coordination through issuance of the agreed incorporation and licensing documents, subject to authority approval."], ["Post-Incorporation Actions", "Where included, we coordinate establishment records, immigration-file steps, initial corporate records, bookkeeping commencement and other agreed actions following licence issuance."]]},
            {"heading": "Corporate Shareholders & International Ownership", "paragraphs": ["Where a shareholder is another company, the authority may require corporate records, ownership information, resolutions and documents in a particular form.", "Cross-border ownership can also affect attestation, translation, beneficial-ownership disclosure and banking preparation. We identify these requirements early and coordinate them within the agreed scope."]},
            {"heading": "What Happens When the Licence Is Issued?", "items": ["Immigration and residence requirements.", "Banking applications.", "Proper financial records.", "Corporate Tax and VAT assessment.", "Beneficial-ownership and corporate records.", "Contracts, premises or operational permissions.", "Licence conditions.", "Renewal dates."], "note": "We provide a post-incorporation action list for the items included in our engagement and can continue managing the agreed workstreams."}
        ], "faq": [["Should I choose mainland or free zone?", "That depends on the activities, customers, operating location, premises, staffing, visas, ownership, banking profile and growth plans."], ["Can a foreign company own the UAE entity?", "Corporate and international ownership may be possible depending on the structure and activity."], ["Is banking included with formation?", "Banking support is a separate workstream unless expressly included in the proposal."], ["Can I form a company only to obtain a visa?", "A business should have a genuine and explainable purpose. Stratos is unlikely to accept an engagement where the only objective is the cheapest licence or residence route with no credible business rationale."]], "cta_label": "READY TO FORM", "cta_heading": "Implement a UAE Structure That Has Been Properly Considered.", "cta_copy": "Tell us the proposed activities, ownership, chosen jurisdiction, if any, and timetable. We will confirm whether formation can begin or whether commercial assessment should come first."
    },
    "accounting_management_reporting": {"path": "/services/accounting-management-reporting/", "title": "UAE Accounting & Management Reporting | Stratos", "meta_description": "UAE bookkeeping, reconciliations, management reporting and year-end preparation for international founders and owner-managed businesses.", "label": "ACCOUNTING & REPORTING", "heading": "Financial Records You Can Actually Use.", "intro": "Bookkeeping and management reporting for UAE companies that need reliable records, clear oversight and properly prepared information for decisions, year-end work and tax coordination.", "secondary": "See What We Cover", "sections": [{"heading": "Accounting Should Begin Before the Backlog Does.", "paragraphs": ["A new company starts creating bookkeeping requirements as soon as it begins entering contracts, paying costs, issuing invoices, receiving funds or moving money between group entities.", "Waiting until a return, audit, bank request or renewal creates urgency usually means reconstructing records under pressure.", "We establish the bookkeeping process early, define what information is required and agree a reporting timetable that reflects the actual business."]}, {"heading": "Core Services", "cards": [["Accounting Set-Up", "Appropriate chart of accounts, opening balances, reporting periods and working processes."], ["Bookkeeping", "Recording and classification of agreed transactions based on information and supporting documentation provided."], ["Bank & Balance-Sheet Reconciliations", "Reconciliation of bank accounts and agreed balance-sheet items so differences and missing information are identified."], ["Receivables & Payables", "Agreed customer and supplier schedules showing amounts due, overdue or awaiting resolution."], ["Management Reporting", "Periodic reporting that may include profit and loss, balance sheet, cash position, receivables, payables and commentary on material movements."], ["Year-End & Audit Preparation", "Closing the accounting period and preparing records and schedules for tax specialists or an appropriately licensed independent auditor where required."]]}, {"heading": "Reporting Designed Around Decisions.", "paragraphs": ["A trading company may need gross margin, inventory and counterparty reporting. A consulting business may need project, cost-centre and receivables visibility. A holding company may require clear intercompany, investment and funding records.", "We agree the reporting structure with the people who will use it. The objective is to give owners and managers information that matches how they assess the business."]}, {"heading": "International Groups", "items": ["Shareholder and related-party balances.", "Intercompany charges and funding.", "Transaction descriptions and supporting agreements.", "Reporting currencies.", "Consolidation timetables.", "Cost allocation.", "Source documents held in different countries.", "Information required by group auditors or tax advisers."], "note": "We can align the UAE bookkeeping process with an agreed group timetable while keeping the local company’s records separately identifiable."}, {"heading": "A Clear Division of Responsibilities.", "paragraphs": ["Stratos maintains records using the information supplied and the scope agreed. The company remains responsible for providing complete, accurate and timely invoices, bank information, contracts, expense support and explanations of transactions.", "Formal tax advice and filing, statutory audit and legal conclusions are not presented as bookkeeping services. Where needed, we coordinate with the appropriately registered or licensed specialist."]}, {"heading": "Moving Existing Accounts to Stratos", "paragraphs": ["We begin with a controlled handover. This may include review of the prior trial balance, ledgers, bank reconciliations, outstanding receivables and payables, tax registrations, filing history and available supporting documents.", "If the records contain gaps or unreconciled balances, remediation work is identified separately rather than hidden within routine monthly fees."]}], "faq": [["How often can management reports be prepared?", "Monthly reporting is common, but frequency depends on transaction volume, management needs and information availability."], ["Can Stratos take over incomplete or overdue accounts?", "Potentially. Historical clean-up is assessed and scoped separately from ongoing bookkeeping."], ["Does bookkeeping include Corporate Tax and VAT returns?", "Not automatically. Formal tax assessment, advice, representation and filing are coordinated with appropriately registered or licensed tax professionals where required."], ["Does Stratos perform statutory audits?", "No. Statutory audits are performed by appropriately licensed independent auditors."], ["Can you work with our existing accounting system or group finance team?", "Usually, subject to suitability and an agreed division of responsibilities."]], "cta_label": "ESTABLISH CONTROL EARLY", "cta_heading": "Put Reliable Financial Information Behind the UAE Business.", "cta_copy": "Tell us whether the company is new or already operating, its transaction volume, current bookkeeping status and the reporting needed by management or the wider group."},
    "business_bank_account_support": {"path": "/services/business-bank-account-support/", "title": "UAE Business Bank Account Support | Stratos Consulting", "meta_description": "UAE business banking support covering bank-fit assessment, business profiles, KYC packs, application preparation and review follow-up.", "label": "BANKING APPLICATION SUPPORT", "heading": "Prepare the Business for the Bank’s Questions.", "intro": "Bank-fit assessment, business-profile development, KYC preparation and application support for UAE companies with international ownership or cross-border operations.", "secondary": "See How Banking Support Works", "sections": [{"heading": "A Bank Account Is an Independent Approval Process.", "paragraphs": ["A UAE trade licence does not create an entitlement to a business bank account. Banks must understand the company, its owners, activities, expected transactions, source of funds, markets and purpose for opening the account.", "Different banks also have different appetites, operating requirements and internal review processes. We help present the business accurately and coherently. We do not promise approval or claim influence over a bank’s decision."]}, {"heading": "What We Assess", "cards": [["The Business Model", "What the company sells, who it serves, where suppliers and customers are based and how commercial activity can be evidenced."], ["Ownership & Control", "Shareholders, ultimate beneficial owners, directors, authorised signatories and intermediate entities."], ["Source of Funds & Source of Wealth", "The origin of company capital and information available to explain the relevant owners’ broader source of wealth."], ["Expected Account Activity", "Currencies, countries, transaction values, frequency, major counterparties and commercial purpose."], ["UAE Connection", "The intended UAE operations, decision-making, premises, employees, residence position and reasons for using a UAE account."], ["Application Readiness", "Whether incorporation records, contracts, invoices, group documents, financial information and ownership evidence are complete and internally consistent."]]}, {"heading": "What the Service Can Include", "cards": [["Bank-Fit Assessment", "Assessment of the company’s profile and practical banking requirements against potential institutions."], ["Readiness Review", "Identification of gaps, inconsistencies or unsupported claims before submission."], ["Business Profile", "Preparation of a clear explanation of the business, ownership, markets, counterparties, expected transactions and UAE rationale."], ["KYC & Application Pack", "Organisation of agreed corporate, ownership, identity, source-of-funds and commercial documents."], ["Interview & Information-Request Preparation", "Preparation of relevant owners or signatories for bank questions and follow-up requests."], ["Liaison & Follow-Up", "Tracking outstanding items and coordinating responses throughout the review."]]}, {"heading": "A Strong Application Is Not One with the Most Documents. It Is One in Which the Facts Agree.", "paragraphs": ["The activity on the licence should be consistent with the business description. The website, contracts and invoices should describe the same commercial model. Expected transactions should make sense for the stated customers, suppliers and capital.", "Our job is to find and resolve avoidable inconsistencies before the bank does."], "note": "We will not guarantee an account, fabricate documents, conceal ownership or recommend inaccurate statements."}], "faq": [["Can Stratos guarantee that the account will be opened?", "No."], ["Which is the best UAE bank for a new company?", "There is no universal answer. The relevant bank depends on the company’s activities, ownership, countries, currencies, transaction profile and required services."], ["How long does the process take?", "Timing varies materially between banks and applications."], ["Can you support foreign corporate shareholders?", "Yes, subject to acceptance and appropriate ownership documentation."], ["Should banking work begin before incorporation?", "Banking considerations should be included during structuring so that the company structure and banking narrative remain aligned."], ["Does a UAE residence visa guarantee banking approval?", "No."]], "cta_label": "PREPARE BEFORE APPLYING", "cta_heading": "Give the Bank a Business It Can Understand.", "cta_copy": "Tell us about the company, owners, markets, expected account activity and current formation status. We will assess whether the profile is ready and where support would add value."},
    "residence_visa_support": {"path": "/services/residence-visa-support/", "title": "UAE Residence Visa Support for Business Owners | Stratos", "meta_description": "UAE residence and visa application and renewal coordination for eligible business owners, employees and dependants.", "label": "RESIDENCE & IMMIGRATION", "heading": "UAE Residence and Visa Support Connected to the Company.", "intro": "Preliminary eligibility review and application or renewal coordination planned around the company’s structure, establishment timetable and genuine staffing requirements.", "secondary": "See What We Coordinate", "sections": [{"heading": "Residence Planning Begins with the Company.", "paragraphs": ["The available residence routes, application sequence and number of visas can depend on the company, licence, ownership, role, premises and current immigration position.", "We establish who requires residence, in what capacity and by when. We then coordinate the applicable process and explain the information, dependencies and external charges involved."]}, {"heading": "Who We Can Support", "cards": [["Owners & Investors", "Coordination of applicable residence processes connected to eligible shareholding or business positions."], ["Employees", "Coordination of employment-related applications and renewals for genuine roles."], ["Dependants", "Support with eligible dependant applications and renewals."], ["Existing Residents", "Coordination of agreed renewals, amendments, cancellations or status-related administrative actions."], ["Golden Residency Applicants", "Preliminary eligibility review and application coordination for applicants who may qualify under current criteria."]]}, {"heading": "What the Service Can Include", "cards": [["Route & Sequence Confirmation", "Confirmation of proposed application category, dependencies and order of steps."], ["Document Checklist", "A case-specific list of identity, company, relationship, qualification or supporting documents."], ["Application Coordination", "Assistance with agreed forms, submissions, appointments and routine follow-up."], ["Medical, Identity & Related Steps", "Coordination of applicable medical screening, Emirates ID and residence issuance steps."], ["Renewal & Expiry Management", "Tracking of agreed expiry dates and planned commencement of renewal procedures."]]}, {"heading": "Built into the Wider Plan.", "paragraphs": ["Residence should not be treated as an isolated final step. The company route may affect visa capacity, and timing can affect when owners or staff relocate.", "Where Stratos manages the wider establishment, these dependencies are coordinated within one implementation timetable."]}], "faq": [["How many visas can a UAE company obtain?", "There is no single number applicable to every company."], ["Can my family obtain UAE residence through me?", "Eligible dependants may be sponsored where applicable requirements are met."], ["Can Stratos guarantee Golden Residency?", "No."], ["Does residence come automatically with company formation?", "No. Formation and residence are connected but separate processes."], ["Can Stratos manage renewals?", "Yes, where renewal and expiry management are included in the engagement."]], "cta_label": "PLAN THE MOVE", "cta_heading": "Coordinate Residence with the Business Timetable.", "cta_copy": "Tell us who requires UAE residence, their relationship to the company, current location and intended timing."},
    "corporate_tax_vat_coordination": {"path": "/services/corporate-tax-vat-coordination/", "title": "UAE Corporate Tax & VAT Coordination | Stratos", "meta_description": "UAE Corporate Tax and VAT readiness, accounting-information preparation and coordination with registered or licensed tax specialists.", "label": "TAX READINESS & COORDINATION", "heading": "Corporate Tax and VAT Work Starts with Reliable Information.", "intro": "Stratos prepares the financial records, supporting information and internal timetable required for tax work, then coordinates formal assessment, advice and filing with appropriately registered or licensed tax professionals.", "secondary": "See How Responsibilities Are Divided", "sections": [{"heading": "One Process, Clear Professional Responsibility.", "paragraphs": ["Tax work often sits between the company, its bookkeeper, management and an external tax specialist. If responsibilities are unclear, records arrive late, questions go unanswered and assumptions are made without the necessary commercial context.", "Stratos coordinates the process while keeping professional responsibility explicit."]}, {"heading": "Corporate Tax Coordination", "cards": [["Readiness Review", "Review of available financial records, registration status, financial period, ownership information and filing timetable."], ["Information Preparation", "Preparation of trial balance, ledgers, reconciliations and agreed supporting schedules."], ["Specialist Coordination", "Management of information flow between the company, Stratos bookkeeping team and appropriately qualified tax professional."], ["Registration & Return Support", "Coordination of information required for Corporate Tax registration, return preparation or agreed submissions."], ["Ongoing Action Tracking", "Maintenance of an agreed timetable for information, review, approval and submission."]]}, {"heading": "VAT Coordination", "cards": [["Registration Assessment Support", "Collection of relevant sales, purchase, import, export and business information for specialist assessment."], ["VAT Accounting Information", "Maintenance and reconciliation of relevant transaction data and supporting documents."], ["Return-Period Preparation", "Preparation of accounting schedules and source information."], ["Specialist Review & Filing", "Coordination with an appropriately qualified tax professional for technical review, advice, filing or representation."]]}, {"heading": "Free Zone Does Not Mean No Tax Work.", "paragraphs": ["A free-zone licence does not remove the need to understand Corporate Tax, VAT, recordkeeping or filing obligations. Treatment depends on the company’s facts, activities, transactions and applicable law.", "Formal conclusions and advice are provided by appropriately qualified tax or legal professionals."]}, {"heading": "International Groups", "items": ["Related-party transactions.", "Intercompany services, loans and funding.", "Ownership and control.", "Cross-border revenue and expenses.", "Supporting agreements.", "Transfer-pricing considerations.", "Permanent-establishment questions.", "Transactions between free-zone and other entities."]}], "faq": [["Does every UAE company need to consider Corporate Tax?", "Every company should establish its position based on its specific circumstances."], ["Does every company need to register for VAT?", "No. Registration depends on the applicable rules and the company’s facts."], ["Can Stratos file Corporate Tax or VAT returns?", "Where filing or formal representation requires a registered or licensed tax professional, that work is handled by the relevant independent specialist."], ["Is tax advice included in monthly bookkeeping?", "No. Bookkeeping and formal tax advice are distinct professional functions."], ["Can you help with missed registrations or returns?", "Potentially. We first establish the records and current position before an appropriate specialist assesses corrective action."]], "cta_label": "PREPARE BEFORE THE DEADLINE", "cta_heading": "Connect the Financial Records to the Tax Work.", "cta_copy": "Tell us whether the company is already operating, its current bookkeeping status, tax registrations, reporting period and any overdue or upcoming requirements."},
    "corporate_administration_governance": {"path": "/services/corporate-administration-governance/", "title": "UAE Company Administration & Governance | Stratos", "meta_description": "UAE licence renewals, company amendments, corporate records, governance calendars and recurring corporate-requirement coordination.", "label": "ONGOING CORPORATE SERVICES", "heading": "Keep the UAE Company Current, Documented and Ready.", "intro": "Ongoing corporate administration and governance coordination for businesses that need more than an annual reminder to renew the licence.", "secondary": "See the Ongoing Scope", "sections": [{"heading": "Incorporation Creates a Company That Must Be Maintained.", "paragraphs": ["Ownership changes. Directors and signatories change. Licences, leases and residence documents expire. Authorities request updated information. Banks and professional advisers ask for current corporate records.", "We maintain an agreed corporate calendar, coordinate routine actions and keep a clear record of what has been completed, what requires approval and what remains outstanding."]}, {"heading": "Licence & Establishment Administration", "items": ["Licence-renewal coordination.", "Review of documents and payments required for renewal.", "Coordination of permitted activity, name, address or other company amendments.", "Immigration-file and establishment-related administrative actions.", "Tracking of agreed authority and workspace dependencies.", "Collection and organisation of updated incorporation and licensing documents."]}, {"heading": "Corporate Records & Governance", "cards": [["Corporate Information", "Maintenance of organised records of the company’s current licence, constitutional documents, ownership, officers, signatories and material authority records."], ["Governance Calendar", "Tracking of agreed renewal dates, recurring actions and other included corporate events."], ["Routine Resolutions & Approvals", "Administrative preparation or coordination of routine shareholder or director approvals within the agreed non-legal scope."], ["Beneficial-Ownership & Control Information", "Coordination of agreed updates and supporting ownership and control records."], ["Adviser & Stakeholder Requests", "Coordination of corporate documents requested by banks, accountants, auditors, tax specialists and other approved parties."]]}, {"heading": "Consider Changes Before Filing.", "paragraphs": ["An apparently simple amendment can affect the licence, ownership records, immigration, banking, contracts, bookkeeping and tax position.", "Before coordinating a material change, we identify the connected workstreams and confirm where legal or tax review is required."]}, {"heading": "A Defined Ongoing Relationship.", "items": ["Which entities are covered.", "Which renewal and governance dates are tracked.", "Which routine actions are included.", "Which information the company must provide.", "Who is authorised to approve instructions.", "Which government and third-party fees are separate.", "Which matters require specialist advice."]}], "faq": [["Can Stratos manage the annual licence renewal?", "Yes, where renewal coordination is included."], ["Can you coordinate changes to shareholders or directors?", "Potentially. The proposed change and related authority, banking, immigration and specialist requirements are reviewed first."], ["Does this service make Stratos a director or company secretary?", "No, unless a separate appointment is expressly agreed and legally permitted."], ["Can you maintain beneficial-ownership information?", "We can coordinate collection, organisation and agreed authority updates."], ["Can existing UAE companies move their administration to Stratos?", "Yes, subject to acceptance and a handover review."]], "cta_label": "CONTINUITY AFTER FORMATION", "cta_heading": "Give the Company One Accountable Administrative Home.", "cta_copy": "Tell us which UAE entity needs support, its renewal date, current records and any expected amendments or governance work."}
}


# Short page names: the big banner heading. The long line becomes the subtitle.
SERVICE_NAMES = {
    "complete_uae_establishment": "Complete UAE Establishment",
    "uae_company_formation": "UAE Company Formation",
    "accounting_management_reporting": "Accounting & Reporting",
    "business_bank_account_support": "Business Banking Support",
    "residence_visa_support": "Residence & Visa Support",
    "corporate_tax_vat_coordination": "Corporate Tax & VAT",
    "corporate_administration_governance": "Corporate Administration",
}
# Image plan per service page (chosen from the images already in /images - see "Image audit" in the README).
#   banner : hero photo          pos : CSS background-position that keeps the calm sky behind the heading
#   bw     : True = black-and-white hero   cta : closing-banner photo
#   splits : photos for the image-left / text-right sections (close-up building shots are fine here
#            because no text ever sits ON these photos)
SERVICE_IMAGES = {
    "complete_uae_establishment": {"banner": "b3.jfif", "pos": "center 0%", "bw": False, "cta": "p4.jfif",
                                   "splits": ["claudio-poggio-0xC7iBAgtr8-unsplash.jpg", "p3.jfif"]},
    "uae_company_formation": {"banner": "p2.jfif", "pos": "center 75%", "bw": True, "cta": "b3.jfif",
                              "splits": ["dubai-7237750_1920.jpg", "p3.jfif"]},
    "accounting_management_reporting": {"banner": "rahul-sharma-auVibNu6bO8-unsplash.jpg", "pos": "center 18%", "bw": True, "cta": "dubai-7237750_1920.jpg",
                                        "splits": ["claudio-poggio-0xC7iBAgtr8-unsplash.jpg", "p3.jfif"]},
    "business_bank_account_support": {"banner": "kate-trysh-70vza4NysS8-unsplash.jpg", "pos": "center 8%", "bw": False, "cta": "p4.jfif",
                                      "splits": ["dubai-7237750_1920.jpg", "p3.jfif"]},
    "residence_visa_support": {"banner": "gabriel-santos-DgLksCjEfB0-unsplash.jpg", "pos": "center 6%", "bw": False, "cta": "b3.jfif",
                               "splits": ["claudio-poggio-0xC7iBAgtr8-unsplash.jpg", "p3.jfif"]},
    "corporate_tax_vat_coordination": {"banner": "amir-hanna-KjWMGF0PYuE-unsplash (1).jpg", "pos": "center 30%", "bw": False, "cta": "dubai-1351569_1920.jpg",
                                       "splits": ["dubai-7237750_1920.jpg", "p3.jfif"]},
    "corporate_administration_governance": {"banner": "b1.jfif", "pos": "center 40%", "bw": False, "cta": "p4.jfif",
                                            "splits": ["claudio-poggio-0xC7iBAgtr8-unsplash.jpg", "p3.jfif"]},
}
for _key, _page in SERVICE_PAGES.items():
    _page["name"] = SERVICE_NAMES[_key]
    _cfg = SERVICE_IMAGES[_key]
    _page["banner_image"], _page["banner_pos"], _page["banner_bw"] = _cfg["banner"], _cfg["pos"], _cfg["bw"]
    _page["cta_image"], _page["split_images"] = _cfg["cta"], _cfg["splits"]


def service_page(key):
    return render_template("service_detail.html", page=SERVICE_PAGES[key])


@app.get("/services/complete-uae-establishment/")
def complete_uae_establishment():
    return service_page("complete_uae_establishment")


@app.get("/services/uae-company-formation/")
def uae_company_formation():
    return service_page("uae_company_formation")


@app.get("/services/accounting-management-reporting/")
def accounting_management_reporting():
    return service_page("accounting_management_reporting")


@app.get("/services/business-bank-account-support/")
def business_bank_account_support():
    return service_page("business_bank_account_support")


@app.get("/services/residence-visa-support/")
def residence_visa_support():
    return service_page("residence_visa_support")


@app.get("/services/corporate-tax-vat-coordination/")
def corporate_tax_vat_coordination():
    return service_page("corporate_tax_vat_coordination")


@app.get("/services/corporate-administration-governance/")
def corporate_administration_governance():
    return service_page("corporate_administration_governance")


@app.get("/faqs")
def faqs():
    return render_template("faqs.html")


# ---------------------------------------------------------------------------
# ARTICLES
# The three cards on /articles used to link to "#". Each one now opens its own
# page. NOTE: article copy is a first draft built from the wording already on
# the service pages - Leah / legal (Palesa, Miguel) should review before launch.
# ---------------------------------------------------------------------------
ARTICLES = {
    "mainland-or-free-zone": {
        "title": "Mainland or Free Zone: Start with How the Business Will Operate",
        "category": "Business Formation",
        "summary": "The practical questions to examine before comparing jurisdictions, authorities or formation packages.",
        "image": "gabriel-santos-DgLksCjEfB0-unsplash.jpg",
        "banner": "p1.jfif",
        "read_time": "4 min read",
        "sections": [
            {"heading": "There is no universally better route", "paragraphs": [
                "Mainland and free-zone companies are often presented as a simple either/or choice, with one described as more flexible and the other as cheaper or faster. In practice, neither statement holds for every business.",
                "The better question is how the company will actually operate: what it will sell, who its customers and suppliers are, where its people and premises will be, and who will own it."]},
            {"heading": "Questions to answer before comparing options", "items": [
                "What activities will the company carry out, and does the licence need to describe each of them?",
                "Where are the customers, suppliers and counterparties based?",
                "Will the business need physical premises, staff or visas in the UAE?",
                "Who will own the company, and is any shareholder another company?",
                "What will the bank need to understand about the business and its expected transactions?",
                "How might the business grow or change over the next few years?"]},
            {"heading": "Why the order matters", "paragraphs": [
                "Comparing authorities or packages before answering those questions tends to produce a structure chosen on price or speed alone. That can leave the business with a licence that does not reflect its activities, ownership documents that are difficult to explain to a bank, or visa capacity that does not match its staffing plans.",
                "At Stratos we establish the commercial facts first, compare the routes that genuinely fit, and record the reasons for the recommendation, including the assumptions and trade-offs involved."]},
        ],
        "service": "complete_uae_establishment",
    },
    "preparing-for-a-uae-bank-account": {
        "title": "How to Prepare for a UAE Business Bank Account Application",
        "category": "Banking",
        "summary": "How ownership, commercial activity, expected transactions and supporting documents shape a corporate account application.",
        "image": "kate-trysh-70vza4NysS8-unsplash.jpg",
        "banner": "rahul-sharma-auVibNu6bO8-unsplash.jpg",
        "read_time": "4 min read",
        "sections": [
            {"heading": "A licence is not an entitlement to a bank account", "paragraphs": [
                "Incorporating a UAE company and opening a corporate bank account are separate processes. A bank decides independently whether to open or maintain an account, and no adviser can guarantee the outcome.",
                "Banks need to understand the company, its owners, its activities, its expected transactions and its reason for using a UAE account."]},
            {"heading": "What a bank will typically want to understand", "items": [
                "The business model: what the company sells, who it serves and where suppliers and customers are based.",
                "Ownership and control: shareholders, ultimate beneficial owners, directors and authorised signatories.",
                "Source of funds and source of wealth.",
                "Expected account activity: currencies, countries, transaction values and major counterparties.",
                "The UAE connection: operations, decision-making, premises and staff."]},
            {"heading": "Make sure the facts agree", "paragraphs": [
                "A strong application is not the one with the most documents. It is one in which the facts agree. The activity on the licence should match the business description, and the website, contracts and invoices should describe the same commercial model.",
                "Finding and resolving avoidable inconsistencies before submission is usually more valuable than adding more paperwork."]},
        ],
        "service": "business_bank_account_support",
    },
    "after-uae-company-incorporation": {
        "title": "What Happens After UAE Company Incorporation?",
        "category": "Compliance",
        "summary": "The bookkeeping, tax, immigration, renewal and governance work that begins once the licence is issued.",
        "image": "dubai-1351569_1920.jpg",
        "banner": "p2.jfif",
        "read_time": "3 min read",
        "sections": [
            {"heading": "The licence is the start, not the finish", "paragraphs": [
                "Once the licence is issued, a number of requirements begin to run at the same time. They are easy to overlook when the focus has been on incorporation."]},
            {"heading": "What typically needs attention", "items": [
                "Immigration and residence requirements.",
                "Banking applications.",
                "Proper financial records and bookkeeping.",
                "Corporate Tax and VAT assessment.",
                "Beneficial-ownership and corporate records.",
                "Contracts, premises or operational permissions.",
                "Licence conditions and renewal dates."]},
            {"heading": "Plan the sequence early", "paragraphs": [
                "These workstreams depend on each other. The company route can affect visa capacity, bookkeeping should begin as soon as the company starts transacting, and renewal dates should be tracked from the outset.",
                "Where Stratos manages the wider engagement, we provide a post-incorporation action list for the items included in the agreed scope and can continue managing those workstreams."]},
        ],
        "service": "corporate_administration_governance",
    },
}


def _unlock_preview():
    key = request.args.get("preview", "")
    if ARTICLES_PREVIEW_KEY and key == ARTICLES_PREVIEW_KEY:
        session["articles_preview"] = True


@app.get("/articles")
def articles():
    _unlock_preview()
    if not articles_visible():
        abort(404)
    return render_template("articles.html", articles=ARTICLES)


@app.get("/articles/<slug>/")
def article_detail(slug):
    _unlock_preview()
    if not articles_visible():
        abort(404)
    article = ARTICLES.get(slug)
    if not article:
        abort(404)
    return render_template("article_detail.html", article=article, slug=slug,
                           service=SERVICE_PAGES[article["service"]],
                           service_endpoint=article["service"])

@app.get("/who-we-work-with")
def who_we_work_with():
    # Merged into the home page (26 Sep review): the page repeated the home page's "Who We Work With" section.
    return redirect(url_for("home") + "#who-we-work-with")

@app.get("/cookie-policy")
def cookie_policy():
    return render_template("cookie_policy.html")

@app.get("/terms")
def terms():
    return render_template("terms.html")


@app.get("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    # The stand-alone Contact page was scrapped (26 Sep review): the Appointments page carries the full enquiry form.
    return redirect(url_for("appointments"))


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    return render_template("appointments.html")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
