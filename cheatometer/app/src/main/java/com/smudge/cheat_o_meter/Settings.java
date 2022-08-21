package com.smudge.cheat_o_meter;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.Toast;
import android.widget.ToggleButton;

public class Settings extends AppCompatActivity {

    private Switch aSwitch;
    private SharedPreferences preferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        aSwitch = findViewById(R.id.camswitch);
        CharSequence cam1 = "D";
        CharSequence cam2 = "A";
        aSwitch.setTextOff(cam1);
        aSwitch.setTextOn(cam2);
        preferences = PreferenceManager.getDefaultSharedPreferences(this);
        if (preferences.getInt("CamMode", 0) == 0) {
            aSwitch.setChecked(false);

        }
        else {
            aSwitch.setChecked(true);
        }

        aSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                Drawable switchcolor;
                SharedPreferences.Editor editor;
                if (b == false){
                    editor = preferences.edit().putInt("CamMode", 0);
                    editor.commit();
                    Toast.makeText(Settings.this, "Default Selected", Toast.LENGTH_SHORT).show();
                }
                else {
                    editor = preferences.edit().putInt("CamMode", 1);
                    editor.commit();
                    Toast.makeText(Settings.this, "Alternate Selected", Toast.LENGTH_SHORT).show();
                }
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {

        return false;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            Settings.this.finish();
            Intent intent = new Intent(Settings.this, MainActivity.class);
            startActivity(intent);
            return true;
        }



        return super.onOptionsItemSelected(item);

    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Settings.this.finish();
        Intent intent = new Intent(Settings.this, MainActivity.class);
        startActivity(intent);

    }
}
