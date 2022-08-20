package com.smudge.cheat_o_meter;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.ViewTreeObserver;
import android.widget.ImageView;
import android.widget.RelativeLayout;

public class SplashScreen extends AppCompatActivity {

public static int acth;
private String logtag = "Splash Screen";
private ImageView logoimage;
private SharedPreferences preferences;
private boolean termsaccepted = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_screen);

        logoimage = (ImageView) findViewById(R.id.logoimage);
        int wt = getResources().getDisplayMetrics().widthPixels;
        Drawable img = getResources().getDrawable(R.drawable.smudgeapp);
        logoimage.setImageDrawable(img);

        preferences = PreferenceManager.getDefaultSharedPreferences(this);
        if (preferences.contains("termsofuseaccepted") == true) {
            if (preferences.getBoolean("termsofuseaccepted", false) == true) {
                termsaccepted = true;
            }
            else {
                termsaccepted = false;
            }
        }
        if (preferences.contains("CamMode") == false) {
            SharedPreferences.Editor editor = preferences.edit().putInt("CamMode", 0);
            editor.commit();
        }


        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (termsaccepted == true) {
                    Intent intent = new Intent(SplashScreen.this, MainActivity.class);
                    startActivity(intent);
                    SplashScreen.this.finish();
                }
                else {
//This condition runs when terms of use have not been accepted by the user and directs them to the relevant screen.
//This is not published version so only directs to main screen in either case.
                    Intent intent = new Intent(SplashScreen.this, MainActivity.class);
                    startActivity(intent);
                    SplashScreen.this.finish();
                }
            }
        }, 1000);
    }
}
