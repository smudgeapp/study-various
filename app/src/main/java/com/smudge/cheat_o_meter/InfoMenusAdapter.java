package com.smudge.cheat_o_meter;


import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;


public class InfoMenusAdapter extends FragmentPagerAdapter {


    public InfoMenusAdapter(FragmentManager fm) {

        super(fm);
    }

    @Override
    public Fragment getItem(int i) {
switch (i) {
    case 1:
        return InfoMenusFragment.newInstance(1, "References");

    case 2:
        return InfoMenusFragment.newInstance(2, "Terms of Use");

     default:
         return InfoMenusFragment.newInstance(0, "Help Guide");
}

    }

    @Override
    public int getCount() {
        return 3;

    }

    @Override
    public CharSequence getPageTitle(int position) {
        if (position == 1) {
            return "References";
        }
        else if (position == 2) {
            return "Terms and Conditions";
        }
        else {
            return "Help Guide";
        }
    }
}
