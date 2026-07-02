const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'rei.deepthought@gmail.com',
    pass: 'xlgl psng hqvp rxfx'
  }
});

const recipient = process.argv[2] || 'wlroderi@yahoo.ca';
const recipientName = process.argv[3] || 'Warren';
const senderName = 'Warren Rodericks';
const senderEmail = 'warren@rodericks.ca'; // placeholder — update if needed

const mailOptions = {
  from: '"Rei 🌟" <rei.deepthought@gmail.com>',
  to: recipient,
  subject: 'Summary of Changes — Bill C-15 (Budget Implementation Act, 2025, No. 1): Insurance Companies Act Amendments',
  html: `
    <div style="font-family: Georgia, serif; max-width: 720px; margin: 0 auto; color: #1a1a1a; padding: 30px; line-height: 1.7;">

      <p>Dear ${recipientName},</p>

      <p>My name is <strong>Rei</strong> — I am an AI assistant working on behalf of <strong>${senderName}</strong>. I was built using a combination of large language models (including Anthropic's Claude), hosted and orchestrated through a platform called <a href="https://openclaw.ai" style="color: #2980b9;">OpenClaw</a>. I help Warren with research, drafting, analysis, and other professional tasks — including preparing and sending briefings like this one.</p>

      <p>Warren asked me to share the following summary of the key changes to the <em>Insurance Companies Act</em> (ICA) introduced by Bill C-15 — the <em>Budget Implementation Act, 2025, No. 1</em>, which received Royal Assent on March 26, 2026.</p>

      <p>The amendments span four divisions and reflect a broader shift in Canadian insurance regulation from prescriptive statutory rules toward principles-based OSFI oversight.</p>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Division 10 — Sunset Provision Extension</h2>
      <p>The statutory deadline requiring federally regulated insurers to be reauthorized by Parliament has been extended to <strong>June 30, 2033</strong> for all companies, insurance holding companies, and fraternal benefit societies. This is routine housekeeping that prevents insurers from technically losing their licences.</p>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Division 11 — Modernizing Prudential Limits on Borrowing, Loans, and Investments</h2>
      <p>This is the most substantive division. The ICA's longstanding <strong>hard statutory limits</strong> on borrowing, commercial lending, real property investment, and equity holdings have been <strong>repealed entirely</strong> across all entity types — life companies, P&C/marine companies, fraternal benefit societies, foreign branches, and insurance holding companies.</p>
      <p>In their place, OSFI gains a discretionary <strong>divestment order</strong> power: if the Superintendent determines that a company's portfolio poses a prudential risk, OSFI may order a reduction in that exposure. There are no longer statutory ceilings — OSFI exercises judgment on a case-by-case basis, consistent with its existing capital adequacy frameworks (LICAT for life companies, MCT for P&C).</p>
      <p><strong>Important:</strong> Division 11 does not come into force on Royal Assent — it takes effect on a date to be fixed by order of the Governor in Council.</p>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Division 12 — Electronic Document Delivery to Policyholders</h2>
      <p>Insurers may now send governance documents (meeting notices, proxy circulars, etc.) to policyholders <strong>electronically by default</strong>, without requiring prior consent. Requirements include:</p>
      <ul>
        <li>Notice of availability following applicable securities rules</li>
        <li>Documents must remain accessible online for at least one year</li>
        <li>Paper copies must be provided on request within 3 business days (before a meeting) or 10 business days (after a meeting)</li>
      </ul>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Division 13 — Widely Held (Public Holding) Threshold</h2>
      <p>The equity threshold above which insurers must have broadly distributed public ownership has been <strong>doubled from $2 billion to $4 billion</strong>. Insurers with equity between $2B and $4B are no longer required to be widely held, giving existing owners greater flexibility around ownership concentration.</p>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Division 14 — OSFI Supervisory Powers</h2>
      <p>Three targeted expansions of OSFI's authority, all effective on Royal Assent:</p>
      <ol>
        <li><strong>Annual Examination Mandate Expanded:</strong> OSFI's annual examination must now assess whether companies have adequate policies and procedures to protect against <em>threats to their integrity or security</em> — cybersecurity and operational resilience are now formal examination criteria.</li>
        <li><strong>New Compliance Direction Power:</strong> OSFI can issue compliance directions specifically where a company's security framework is inadequate, independent of any finding of financial unsoundness or unsafe practice.</li>
        <li><strong>Information Sharing with Federal Agencies:</strong> OSFI may now share supervisory information with any federal government agency for purposes related to financial institution supervision, integrity/security threats, or <em>national security</em> — a new and notable carve-out.</li>
      </ol>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <h2 style="font-size: 18px; color: #2c3e50;">Overall Observation</h2>
      <p>The through-line across these amendments is a shift from the <strong>prescriptive, rules-based</strong> framework established in the original 1991 ICA toward a <strong>principles-based supervisory model</strong> where OSFI exercises considerably more discretion. This aligns with the broader trajectory of international financial regulation (Basel III, IFRS 17, Solvency II) and places greater weight on OSFI's judgment in managing the risk profile of the Canadian insurance sector.</p>

      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />

      <p>If you have any questions about this briefing, please direct them to <strong>${senderName}</strong> directly. As an AI assistant, I am not able to monitor or respond to email.</p>

      <p style="margin-top: 32px;">
        Regards,<br/>
        <strong>Rei</strong><br/>
        <em>AI Assistant to ${senderName}</em>
      </p>

      <p style="font-size: 12px; color: #999; margin-top: 40px; border-top: 1px solid #eee; padding-top: 16px;">
        This message was prepared and sent by Rei, an AI assistant, on behalf of ${senderName}. For questions or follow-up, please contact ${senderName} directly.
      </p>
    </div>
  `
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.error('Error:', error);
    process.exit(1);
  } else {
    console.log('Sent:', info.messageId);
    console.log('To:', recipient);
  }
});
