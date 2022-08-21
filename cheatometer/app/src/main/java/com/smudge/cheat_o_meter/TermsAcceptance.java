package com.smudge.cheat_o_meter;

import android.Manifest;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.preference.PreferenceManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

//The screen to get user consent to terms and conditions of use.

public class TermsAcceptance extends AppCompatActivity {

    private WebView terms;
    private TextView link;
    private WebView agreement;
    private Button accept;
    private Button notaccept;
    private SharedPreferences preferences;
    private SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_terms_acceptance);

        terms = (WebView) findViewById(R.id.terms);
        terms.setBackgroundColor(Color.BLACK);
        link = (TextView) findViewById(R.id.link);
        link.setTextColor(Color.BLUE);
        link.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent termspage = new Intent(TermsAcceptance.this, TermsandConditions.class);
                startActivity(termspage);
            }
        });
        agreement = findViewById(R.id.agreement);
        agreement.setBackgroundColor(Color.BLACK);
        accept = findViewById(R.id.accept);
        accept.setTextColor(Color.WHITE);
        notaccept = findViewById(R.id.notaccept);
        notaccept.setTextColor(Color.WHITE);
        setTexts();

        preferences = PreferenceManager.getDefaultSharedPreferences(this);
        accept.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (ContextCompat.checkSelfPermission(TermsAcceptance.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED ||
                        ContextCompat.checkSelfPermission(TermsAcceptance.this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                    if (ActivityCompat.shouldShowRequestPermissionRationale(TermsAcceptance.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == true ||
                            ActivityCompat.shouldShowRequestPermissionRationale(TermsAcceptance.this, Manifest.permission.READ_EXTERNAL_STORAGE) == true) {
                        AlertDialog.Builder termspermission = new AlertDialog.Builder(TermsAcceptance.this);
                        termspermission.setTitle("Permission Required").setMessage("Data Collection process stores the user input data on the device till next background collection " +
                                "is scheduled. This data is removed from the device after collection is complete. Permission is required to proceed. " +
                                "Please provide the required permissions.").
                                setPositiveButton("Allow Permission", new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialogInterface, int i) {
                                        ActivityCompat.requestPermissions(TermsAcceptance.this, new String[] {Manifest.permission.READ_EXTERNAL_STORAGE,
                                        Manifest.permission.WRITE_EXTERNAL_STORAGE}, 2);
                                    }
                                })
                                .setNegativeButton("Deny Permission", new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialogInterface, int i) {
                                        editor = preferences.edit().putBoolean("termsofuseaccepted", false);
                                        editor.commit();
                                        finish();
                                        dialogInterface.cancel();
                                    }
                                });
                        termspermission.create().show();
                    }
                    else {
                        ActivityCompat.requestPermissions(TermsAcceptance.this, new String[] {Manifest.permission.READ_EXTERNAL_STORAGE,
                                Manifest.permission.WRITE_EXTERNAL_STORAGE}, 2);
                    }
                }
                else {
                    editor = preferences.edit().putBoolean("termsofuseaccepted", true);
                    editor.commit();
                    Toast.makeText(TermsAcceptance.this, "Thank You. Enjoy!", Toast.LENGTH_LONG).show();
                    Intent intent = new Intent(TermsAcceptance.this, MainActivity.class);
                    startActivity(intent);
                    TermsAcceptance.this.finish();
                }

            }
        });

        notaccept.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                editor = preferences.edit().putBoolean("termsofuseaccepted", false);
                editor.commit();
                finish();

            }
        });


    }

    private void setTexts() {
        String texts = "<html><body><p align=\"justify\"><font size=\"2\" color=\"white\">";
        String texte = "</font></p></body></html>";

        String termsbrief = "Please read and accept the Terms and Conditions of Use and the Privacy Policy, contained therein, before using Cheat-O-Meter.";

        terms.loadData(texts + termsbrief + texte, "text/html", "utf-8");

        String termsagreement = "I have read and accept the Terms and Conditions of Use and the Privacy Policy, contained therein.";

        agreement.loadData(texts + termsagreement + texte, "text/html", "utf-8");



    }

    @Override
    public void onRequestPermissionsResult(int requestcode, String permissions[], int[] grantresult) {
        if (requestcode == 2) {
            if (grantresult.length > 0 && grantresult[0] == PackageManager.PERMISSION_GRANTED && grantresult[0] == PackageManager.PERMISSION_GRANTED) {
                editor = preferences.edit().putBoolean("termsofuseaccepted", true);
                editor.commit();
                Toast.makeText(TermsAcceptance.this, "Thank You. Enjoy!", Toast.LENGTH_LONG).show();
                Intent intent = new Intent(TermsAcceptance.this, MainActivity.class);
                startActivity(intent);
                TermsAcceptance.this.finish();
           }
           else {
                editor = preferences.edit().putBoolean("termsofuseaccepted", false);
                editor.commit();
                finish();
            }

        }
    }
}
