package com.smudge.cheat_o_meter;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;

public class HelpInfo extends AppCompatActivity implements InfoMenusFragment.OnListFragmentInteractionListener {

    private ViewPager pager;
    private InfoMenusAdapter adapter;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_help_info);

        pager = (ViewPager) findViewById(R.id.pager);
        adapter = new InfoMenusAdapter(getSupportFragmentManager());
        pager.setAdapter(adapter);


    }

    @Override
    public void onListFragmentInteraction(String item) {

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {

        return false;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {

            Intent intent = new Intent(HelpInfo.this, MainActivity.class);
            startActivity(intent);
            HelpInfo.this.finish();
            return true;
        }



        return super.onOptionsItemSelected(item);

    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();

        Intent intent = new Intent(HelpInfo.this, MainActivity.class);
        startActivity(intent);
        HelpInfo.this.finish();

    }
}
