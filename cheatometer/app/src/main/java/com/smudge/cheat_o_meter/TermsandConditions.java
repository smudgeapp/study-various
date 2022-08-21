package com.smudge.cheat_o_meter;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;

public class TermsandConditions extends AppCompatActivity {

    private WebView terms;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_termsand_conditions);

        terms = findViewById(R.id.terms);
        String texts = "<html><body><p align=\"justify\">";
        String texte = "</p></body></html>";
        String toutext = "<b>TERMS AND CONDITIONS OF USE</b><br/>";
        terms.loadData(texts + toutext + texte, "text/html", "utf-8");

    }
}
