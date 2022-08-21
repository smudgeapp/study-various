package com.smudge.cheat_o_meter;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;

/**
 * A fragment representing a list of Items.
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnListFragmentInteractionListener}
 * interface.
 */
public class InfoMenusFragment extends Fragment {

    // TODO: Customize parameter argument names
    private static final String COLUMN_COUNT = "column-count";
    private static final String PAGE_TITLE = "pagetitle";
    // TODO: Customize parameters
    private int mColumnCount = 1;
    private OnListFragmentInteractionListener mListener;
    private WebView infotexts;

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public InfoMenusFragment() {}


    // TODO: Customize parameter initialization
    @SuppressWarnings("unused")
    public static InfoMenusFragment newInstance(int columnCount, String title) {
        InfoMenusFragment fragment = new InfoMenusFragment();
        Bundle args = new Bundle();
        args.putInt(COLUMN_COUNT, columnCount);
        args.putString(PAGE_TITLE, title);
        fragment.setArguments(args);
        return fragment;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_infomenus_list, container, false);
        infotexts = (WebView) view.findViewById(R.id.infotexts);
        if (getArguments() != null) {
            mColumnCount = getArguments().getInt(COLUMN_COUNT);
            setInfo(mColumnCount);

        }

        // Set the adapter

        return view;
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (getArguments() != null) {
            mColumnCount = getArguments().getInt(COLUMN_COUNT);

        }


    }



    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof OnListFragmentInteractionListener) {
            mListener = (OnListFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnListFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    private void setInfo(int columnid) {
        String texts = "<html><body><p align=\"justify\">";
        String texte = "</p></body></html>";

        String helptext;
        String reftext;
        String toutext;
        switch (columnid) {
            case 0:
            helptext = "Cheat-O-Meter is intended for entertainment purposes only. It performs certain tests which are based on scientific research (Refer to References) but its results should NOT be taken as confirmation of personality and/or behavioral/attitudinal traits of the person(s) being tested. <br/>" +
                    "<br/>" +
                    "Please ensure that you have read the Terms of Use and the Privacy Policy, contained therein, prior to using the app. Additionaly, you may also want to refer to the references. <br/>" +
                    "<br/>" +
                    "<b>F Button:</b> Activates the Face Test screen.<br/>" +
                    "<br/>" +
                    "<b>Q Button:</b> Activates the Questionnaire screen.<br/>" +
                    "<br/>" +
                    "<b>C Button:</b> Activates the Combine Test screen. This button activates only after one test has been done. If a Face Test has been done first, it will activate the Questionnaire screen and vice versa. <br/>" +
                    "<br/>" +
                    "<b>R Button:</b> Resets the Cheat-O-Meter.<br/>" +
                    "<br/>" +
                    "<b>Face Test Screen:</b> Face Test screen uses the device camera to detect a face and extract required dimensions to perform the Cheat-O-Meter test. <br/>" +
                    "<br/>" +
                    "When required dimensions are available, Check button at the bottom of the Face Test screen will turn green, indicating that the test may be performed now. <br/>" +
                    "<br/>" +
                    "Additional buttons on the Face Test screen provides, zoom functionality, switching camera (front or back) and toggle flash. <br/>" +
                    "<br/>" +
                    "If F Button is pressed while the Face Test screen is active, it will deactivate.<br/>" +
                    "<br/>" +
                    "<b>Questionnaire Screen:</b> Questionnaire includes six multiple choice questions based on which Cheat-O-Meter test is performed. If no option is selected before closing the screen, the test is not performed.<br/>" +
                    "<br/>" +
                    "If Q Button is pressed while the Questionnaire screen is active, it will deactivate.<br/>" +
                    "<br/>" +
                    "<b>Combined Test:</b> Combine Test combines the values from both the tests to return a total result. <br/>" +
                    "<br/>" +
                    "<b>Did They Do It?:</b> This is an additional question which activates when a test has been performed. This is an optional question and has no effect on the test results. <br/>" +
                    "<br/>" +
                    "This information, if the user chooses to provide, will be used to improve the results of the Cheat-O-Meter tests. Refer to the Terms and Conditions of Use and the Privacy Policy contained therein to find out more.";
            infotexts.loadData(texts + helptext + texte, "text/html", "utf-8");
                break;
            case 1:
                reftext = "Ajzen, I. (1991). The Theory of Planned Behavior. <i>Organizational Behavior and Human Decision Processes, 50</i>, 179&ndash;211.<br/>" +
                        "<br/>" +
                        "Ajzen, I. (2002). Constructing a TpB Questionnaire: Conceptual and Methodological Considerations. <i>Institute for Interdisciplinary Research on Conflict and Violence: Universitat Bielefeld</i>, 14.<br/>" +
                        "<br/>" +
                        "Ajzen, I. (2012). The Theory of Planned Behavior. <i>In Handbook of Theories of Social Psychology</i> (pp. 438&ndash;459). New York: Lawrence Erlbaum Association. <br/>" +
                        "<br/>" +
                        "Arnocky, S., Carre, J. M., Bird, B. M., Moreau, B. J. P., Vaillancourt, T., Ortiz, T., & Marley, N. (2018). The Facial Width-to-Height Ratio Predicts Sex Drive, Sociosexuality, and Intended Infidelity. <i>Archives of Sexual Behavior, 47</i>(5), 1375&ndash;1385.<br/>" +
                        "<br/>" +
                        "Buunk, B. P., & Bakker, A. B. (1995). Extradyadic Sex: The Role of Descriptive and Injunctive Norms. <i>The Journal of Sex Research, 32</i>(4), 313&ndash;318. https://doi.org/10.1080/00224499509551804 <br/>" +
                        "<br/>" +
                        "Jackman, M. (2015). Understanding the Cheating Heart: What Determines Infidelity Intentions? <i>Sexuality and Culture, 19</i>(1), 72&ndash;84.<br/>" +
                        "<br/>" +
                        "Rhodes, G., Morley, G., & Simmons, L. W. (2013). Women can judge sexual unfaithfulness from unfamiliar men&rsquo;s faces. <i>Biology Letters  &ndash; Royal Society Publishing, 9</i>(1). https://doi.org/10.1098/rsbl.2012.0908<br/>" +
                        "<br/>" +
                        "Tagler, M. J., & Jeffers, H. M. (2013). Sex Differences in Attitudes toward Partner Infidelity. <i>Evolutionary Psychology, 11</i>(4), 821&ndash;832.<br/>" +
                        "<br/>" +
                        "Toplu&ndash;Demirtas, E., & Fincham, F. D. (2018). Dating Infidelity in Turkish Couples: The Role of Attitudes and Intentions. <i>The Journal of Sex Research, 55</i>(2), 252&ndash;262. https://doi.org/10.1080/00224499.2017.1365110<br/>" +
                        "<br/>" +
                        "Wilson, K., Mattingly, B. A., Clark, E. M., Weidler, D. J., & Bequette, A. W. (2011). The Gray Area: Exploring Attitudes Toward Infidelity and the Development of the Perceptions of Dating Infidelity Scale. <i>The Journal of Social Psychology, 151</i>(1), 63&ndash;86<br/>" +
                         "<br/>" +
                          "Zhang, W., Hahn, A. C., Cal, Z., Lee, A. J., Holzeitner, I. J., DeBruine, L. M., & Jones, B. C. (2018). No evidence that facial width-to-height ratio (fWHR) is associated with women&rsquo;s sexual desire. <i>PLoS ONE, 13</i>(7). https://doi.org/10.1371/journal. pone.0200308.";
                    infotexts.loadData(texts + reftext + texte, "text/html", "utf-8");
                    break;

            case 2:
                toutext = "<b>1. TERMS AND CONDITIONS OF USE</b><br/>" +
                        "<br/>" +
                        "By downloading, accessing or using this mobile application (&#34Cheat-O-Meter&#34), you agree to be bound by these Terms and Conditions of Use. The Developer (as defined in Clause 2 of these Terms and Conditions of Use) reserves the right to amend these terms and conditions at any time. If you disagree with any of these Terms and Conditions of Use, you must immediately discontinue your access to the Cheat-O-Meter. Continued use of the Cheat-O-Meter will constitute acceptance of these Terms and Conditions of Use, as may be amended from time to time.<br/>" +
                        "<br/>" +
                        "<b>2. DEFINITIONS</b><br/>" +
                        "<br/>" +
                        "In these Terms and Conditions of Use, the following terms shall have the following meanings, except where the context otherwise requires:<br/>" +
                        "<br/>" +
                        "<b>&#34Mobile Application&#34</b> means the Cheat-O-Meter mobile application.<br/>" +
                        "<br/>" +
                        "<b>&#34Developer&#34</b> means the developer of the Mobile Application, identified by the name &#34Smudge App&#34 on the distribution channel Google Play Store.<br/>" +
                        "<br/>" +
                        "<b>&#34Users&#34</b> means users of the Mobile Application, including you and &#34User&#34 means any one of them.<br/>" +
                        "<br/>" +
                        "<b>&#34Input Data&#34</b> means data input by the User(s) and collected through this Mobile Application as defined in Clause 10.2.1 and 10.2.2 of these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "<b>&#34Data Collection&#34</b> means ONLY the Input Data collected by the Developer through this Mobile Application, in the manner mentioned in Clause 10.2.3, through the third-party service mentioned in Clause 10.2.6, for the purposes mentioned in Clause 10.2.4 and under the retention policy as mentioned in Clause 10.2.5 of these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "<b>&#34Privacy Policy&#34</b> means the privacy policy set out in Clause 10 of these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "<b>3. GENERAL ISSUES ABOUT THE MOBILE APPLICATION</b><br/>" +
                        "<br/>" +
                        "3.1 <i>Applicability of terms and conditions</i>: The use of the Mobile Application is subject to these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "3.2 <i>Equipment and Networks</i>: The provision of the Services and the Mobile Application does not include the provision of a mobile telephone or handheld device or other necessary equipment to access the Mobile Application. The Mobile Application will require Internet connectivity and appropriate telecommunication links from time to time. You acknowledge that the terms of agreement with your respective mobile network provider and/or internet service provider (collectively &#34Internet Provider&#34) will continue to apply when using the Mobile Application. As a result, you may be charged by the Internet Provider for access to network connection services for the duration of the connection for which the Mobile Application requires such network connection, or any such third party charges as may arise. You accept responsibility for any such charges that arise.<br/>" +
                        "<br/>" +
                        "3.3 <i>Permission to use Mobile Application</i>: If you are not the bill payer for the mobile telephone or handheld device being used to access the Mobile Application, you will be assumed to have received permission from the bill payer for using the Mobile Application.<br/>" +
                        "<br/>" +
                        "3.4 <i>License to Use Material</i>: By submitting Input Data via the Application, you represent that you are the owner of the Input Data, or have proper authorization from the owner of the Input Data to use, reproduce and distribute it. You hereby grant the Developer a worldwide, royalty-free, non-exclusive license to use the Input Data to promote any products or services.<br/>" +
                        "<br/>" +
                        "<b>4. YOUR OBLIGATIONS</b><br/>" +
                        "<br/>" +
                        "4.1 <i>Limitation of usage of the Mobile Application</i>: This Mobile Application is intended for ENTERTAINMENT purposes only and should be treated as such. It does calculations on certain behavioral/attitudinal/personality traits and/or physical characteristics based on scientific research. This calculation is done on input provided by the User. This DOES NOT provide any confirmed evidence regarding any person&rsquo;s(s&rsquo;) personality and/or attitudes and behavior.<br/>" +
                        "<br/>" +
                        "4.2 <i>Prohibitions in relation to usage of the Mobile Application</i>: Without limitation, you undertake not to use or permit anyone else to use the Mobile Application:-<br/>" +
                        "<br/>" +
                        "4.2.1 to intercept or attempt to intercept any communications transmitted by way of a telecommunications system;<br/>" +
                        "<br/>" +
                        "4.2.2 for a purpose other than which the Developer has designed it or intended it to be used;<br/>" +
                        "<br/>" +
                        "4.2.3 for any fraudulent purpose;<br/>" +
                        "<br/>" +
                        "4.2.4 other than in conformance with accepted Internet practices and practices of any connected networks;<br/>" +
                        "<br/>" +
                        "4.2.5 attempt to circumvent the Developer&rsquo;s and any third-party services&rsquo; (being employed by the Developer) security or network including to access data not intended for you, log into a server or account you are not expressly authorized to access, or probe the security of other networks;<br/>" +
                        "<br/>" +
                        "4.2.6 execute any form of network monitoring which will intercept data not intended for you;<br/>" +
                        "<br/>" +
                        "4.2.7 extract data from or hack into the Mobile Application;<br/>" +
                        "<br/>" +
                        "4.2.8 use the Services or Mobile Application in breach of these Terms and Conditions of Use;<br/>" +
                        "<br/>" +
                        "4.2.9 engage in any unlawful activity in connection with the use of the Mobile Application or the Services; or<br/>" +
                        "<br/>" +
                        "4.2.10 engage in any conduct which, in the Developer&rsquo;s exclusive reasonable opinion, restricts or inhibits any other customer from properly using or enjoying the Mobile Application.<br/>" +
                        "<br/>" +
                        "<b>5. RULES ABOUT USE OF THE SERVICE AND THE MOBILE APPLICATION</b><br/>" +
                        "<br/>" +
                        "5.1 The Developer will use reasonable endeavors to correct any errors or omissions as soon as practicable after being notified of them. However, the Developer does not guarantee that the Mobile Application will be free of faults, and does not accept liability for any such faults, errors or omissions. In the event of any such error, fault or omission, you should report it by contacting the Developer at email address: smudgeapp@gmail.com.<br/>" +
                        "<br/>" +
                        "5.2 The Developer does not give any warranty that the Mobile Application is free from viruses or anything else which may have a harmful effect on any technology.<br/>" +
                        "<br/>" +
                        "5.3 The Developer reserves the right to change, modify, substitute, suspend or remove without notice any information or service on the Mobile Application from time to time. The Developer reserves the right to withdraw any information from the Mobile Application at any time.<br/>" +
                        "<br/>" +
                        "5.4 The Developer reserves the right to block access to and/or to edit or remove any material which in their reasonable opinion may give rise to a breach of these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "<b>6. DISCLAIMER AND EXCLUSION OF LIABILITY</b><br/>" +
                        "<br/>" +
                        "6.1 The Mobile Application, the information on the Mobile Application and use of all related facilities are provided on an &#34as is, as available&#34 basis without any warranties whether express or implied.<br/>" +
                        "<br/>" +
                        "6.2 To the fullest extent permitted by applicable law, the Developer disclaims all representations and warranties relating to the Mobile Application and its contents.<br/>" +
                        "<br/>" +
                        "6.3 The Developer does not warrant that the Mobile Application will always be accessible, uninterrupted, timely, secure, error free or free from computer virus or other invasive or damaging code or that the Mobile Application will not be affected by any acts of God or other force majeure events, including inability to obtain or shortage of necessary materials, equipment facilities, power or telecommunications, lack of telecommunications equipment or facilities and failure of information technology or telecommunications equipment or facilities.<br/>" +
                        "<br/>" +
                        "6.4 While the Developer may use reasonable efforts to include accurate and up-to-date information on the Mobile Application, they make no warranties or representations as to its accuracy, timeliness or completeness.<br/>" +
                        "<br/>" +
                        "6.5 The Developer shall not be liable for any acts or omissions of any third parties howsoever caused, and for any direct, indirect, incidental, special, consequential or punitive damages, howsoever caused, resulting from or in connection with the Mobile Application, your access to, use of or inability to use the Mobile Application, inaccuracies in the information including but not limited to damages for loss of business or profits, use, data or other intangible, even if the Developer has been advised of the possibility of such damages.<br/>" +
                        "<br/>" +
                        "6.6 The Developer shall not be liable in contract, tort (including negligence or breach of statutory duty) or otherwise howsoever and whatever the cause thereof, for any indirect, consequential, collateral, special or incidental loss or damage suffered or incurred by you in connection with the Mobile Application and these Terms and Conditions of Use. For the purposes of these Terms and Conditions of Use, indirect or consequential loss or damage includes, without limitation, loss of revenue, profits, anticipated savings or business, loss of data or goodwill, loss of use or value of any equipment including software, claims of third parties, and all associated and incidental costs and expenses.<br/>" +
                        "<br/>" +
                        "6.7 The above exclusions and limitations apply only to the extent permitted by law. None of your statutory rights as a consumer that cannot be excluded or limited are affected.<br/>" +
                        "<br/>" +
                        "6.8 Notwithstanding the Developer&rsquo;s efforts to ensure that their system is secure, you acknowledge that all electronic data transfers are potentially susceptible to interception by others. The Developer cannot, and does not, warrant that data transfers pursuant to the Mobile Application, or electronic mail transmitted to and from the Developer, will not be monitored or read by others.<br/>" +
                        "<br/>" +
                        "<b>7. INDEMNITY</b><br/>" +
                        "<br/>" +
                        "You agree to indemnify and keep the Developer indemnified against any claim, action, suit or proceeding brought or threatened to be brought against the Developer which is caused by or arising out of (a) your use of the Mobile Application, (b) any other party&rsquo;s use of the Mobile Application using your name and/or any other identifier, and/or (c) your breach of any of these Terms and Conditions of Use, and to pay the Developer damages, costs and interest in connection with such claim, action, suit or proceeding.<br/>" +
                        "<br/>" +
                        "<b>8. AMENDMENTS</b><br/>" +
                        "<br/>" +
                        "8.1 The Developer may periodically make changes to the contents of the Mobile Application, at any time and without notice. The Developer assumes no liability or responsibility for any errors or omissions in the content of the Mobile Application.<br/>" +
                        "<br/>" +
                        "8.2 The Developer reserves the right to amend these Terms and Conditions of Use from time to time without notice. The revised Terms and Conditions of Use will be posted on the Mobile Application and shall take effect from the date of such posting. You are advised to review these terms and conditions periodically as they are binding upon you.<br/>" +
                        "<br/>" +
                        "<b>9. APPLICABLE LAW AND JURISDICTION</b><br/>" +
                        "<br/>" +
                        "9.1 The Mobile Application can be accessed from all countries around the world where the local technology permits. As each of these places have differing laws, by accessing the Mobile Application both you and the Developer agree that the laws of the Islamic Republic of Pakistan, without regard to the conflicts of laws principles thereof, will apply to all matters relating to the use of the Mobile Application.<br/>" +
                        "<br/>" +
                        "13.2 You accept and agree that both you and the Developer shall submit to the exclusive jurisdiction of the courts of the Islamic Republic of Pakistan in respect of any dispute arising out of and/or in connection with these Terms and Conditions of Use.<br/>" +
                        "<br/>" +
                        "<b>10. PRIVACY POLICY</b><br/>" +
                        "<br/>" +
                        "10.1 Access to the Mobile Application and use of the Mobile Application is subject to this Privacy Policy. By accessing the Mobile Application and by continuing to use the Services offered, you are deemed to have accepted this Privacy Policy, and in particular, you are deemed to have consented to the Developer&rsquo;s use and disclosure of data in the manner prescribed in this Privacy Policy. The Developer reserves the right to amend this Privacy Policy from time to time. If you disagree with any part of this Privacy Policy, you must immediately discontinue your access to the Mobile Application.<br/>" +
                        "<br/>" +
                        "10.2 As part of the normal operation of this Mobile Application, the Developer collects, uses and discloses ONLY THE INPUT DATA in the Mobile Application to third parties. Accordingly, the Developer has developed this Privacy Policy in order for you to understand how the data is collected, used, communicated and disclosed and made use of when you use the Mobile Application.<br/>" +
                        "<br/>" +
                        "10.2.1 Data Collection DOES NOT INCLUDE PERSONAL AND/OR SENSITIVE INFORMATION. Personal and/or Sensitive Information includes, personally identifiable information, financial and payment information, authentication information, phonebook, contacts SMS and call related data, microphone and camera sensor data (camera sensor data EXCLUDES the data described in Clause 10.2.2), and sensitive device or usage data.<br/>" +
                        "<br/>" +
                        "10.2.2 Data Collection is exclusively limited to the data input provided in the Mobile Application by the User as part of its normal use. This includes, and is limited to, image dimensions (and NOT the image itself or any other data obtained from the camera sensor) and questionnaire responses, wherever they may be included in the Mobile Application.<br/>" +
                        "<br/>" +
                        "10.2.3 Data is collected as a background operation scheduled on the User&rsquo;s(s&rsquo;) device(s), from time to time. User will be notified through Mobile Application notifications when this data is being collected and when Data Collection is complete.<br/>" +
                        "<br/>" +
                        "10.2.4 This data is collected to improve the result outputs displayed under the normal use of the Mobile Application, for research and/or commercial purposes, to be shared and/or sold to third parties and any other purposes as required by the Developer.<br/>" +
                        "<br/>" +
                        "10.2.5 Collected data will be retained indefinitely.<br/>" +
                        "<br/>" +
                        "10.2.6 The Developer employs third party companies and/or individuals to facilitate its service (&#34service providers&#34), to provide the service on Developer&rsquo;s behalf, to perform service-related services.<br/>" +
                        "<br/>" +
                        "These third parties HAVE ACCESS TO USER PERSONAL DATA only to perform these tasks on Developer&rsquo;s behalf and are obligated not to disclose or use it for any other purpose.<br/>" +
                        "<br/>" +
                        "<i>Firebase</i><br/>" +
                        "<br/>" +
                        "Firebase Realtime Database is a service provided by Google Inc.<br/>" +
                        "<br/>" +
                        "It is encouraged that the User review Firebase security and privacy policies and what type of information Firebase accesses: <a href=\"https://firebase.google.com/support/privacy/\">Privacy and Security in Firebase</a><br/>" +
                        "<br/>" +
                        "(f) Mobile Application may contain links to other sites that are not operated by the Developer. If you click on a third party link, you will be directed to that third party&rsquo;s site. The Developer strongly advises you to review the Privacy Policy of every site you visit.<br/>" +
                        "<br/>" +
                        "The Developer has no control over and assumes no responsibility for the content, privacy policies or practices of any third party sites or services.<br/>" +
                        "<br/>" +
                        "The Developer is committed to conducting business in accordance with these principles in order to ensure that the confidentiality of personal information is protected and maintained.";
                infotexts.loadData(texts + toutext + texte, "text/html", "utf-8");
                break;

            default:
                break;

        }

    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnListFragmentInteractionListener {
        // TODO: Update argument type and name
        void onListFragmentInteraction(String item);
    }
}
