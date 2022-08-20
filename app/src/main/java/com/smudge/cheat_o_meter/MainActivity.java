package com.smudge.cheat_o_meter;

import android.Manifest;
import android.animation.PropertyValuesHolder;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.hardware.Camera;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewTreeObserver;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;


import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.InterstitialAd;
import com.google.android.gms.ads.MobileAds;

import java.security.Permission;
import java.text.DecimalFormat;
import java.util.List;


public class MainActivity extends AppCompatActivity implements CamActivity.OnFragmentInteractionListener, QsActivity.OnQsFragmentInteractionListener {

private ControlButton fbutton;
private ControlButton qbutton;
private ControlButton cbutton;
private ControlButton rbutton;
private FragmentManager manager;
private FullMeter fullMeter;
private Pointer pointer;
private MeterText mtext;
private TextView mtextin;
private RelativeLayout mainlayout;
private ResponseText rsptext;
private ResponseButton ybtn;
private ResponseButton nbtn;
private String testchk = "";
private String activfragment = "";
private int _id = Integer.MIN_VALUE;
private double mfwhr;
private double mintn;
private CamActivity camActivity;
private QsActivity qsActivity;
private boolean isresponselit = false;
private CollectedData maindb;
private SharedPreferences preferences;
private LinearLayout adlayout;
private RunAds runads;
private TextView percent;
private DecimalFormat d;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_main);

        mainlayout = (RelativeLayout) findViewById(R.id.mainlayout);
        fullMeter = (FullMeter) findViewById(R.id.fullmeter);
        fbutton = (ControlButton) findViewById(R.id.fbutton);
        fbutton.setImage(R.mipmap.fbutton_fg);
        qbutton = (ControlButton) findViewById(R.id.qbutton);
        qbutton.setImage(R.mipmap.qbutton_fg);
        cbutton = (ControlButton) findViewById(R.id.cbutton);
        cbutton.setImage(R.mipmap.cbutton_fg);
        rbutton = (ControlButton) findViewById(R.id.rbutton);
        rbutton.setImage(R.mipmap.rbutton_fg);
        ViewTreeObserver observer = mainlayout.getViewTreeObserver();
        observer.addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener() {
            @Override
            public void onGlobalLayout() {
                Rect rect = new Rect();
                mainlayout.getGlobalVisibleRect(rect);
                int ht  = rect.height();
                fullMeter.setMinimumHeight(ht);
                fullMeter.setBottom(ht);

                   }
        });
        pointer = (Pointer) findViewById(R.id.pointer);
        mtext = (MeterText) findViewById(R.id.mtext);
        mtextin = findViewById(R.id.mtextin);
        mtextin.setTextColor(Color.WHITE);
        percent = findViewById(R.id.percent);
        percent.setTextColor(Color.WHITE);
        rsptext = (ResponseText) findViewById(R.id.rspnsetext);
        ybtn = (ResponseButton) findViewById(R.id.yesbtn);
        ybtn.setBImg(R.drawable.ybutton);
        ybtn.setClickable(false);
        nbtn = (ResponseButton) findViewById(R.id.nobtn);
        nbtn.setBImg(R.drawable.nbutton);
        nbtn.setClickable(false);
        manager = getSupportFragmentManager();
        maindb = new CollectedData(this);
        maindb.open();
        setButtons();
        preferences = getPreferences(MODE_PRIVATE);

        if (this.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA) == false) {
            fbutton.setClickable(false);
            AlertDialog.Builder cmbnull = new AlertDialog.Builder(MainActivity.this);
            cmbnull.setTitle("Camera Not Detected").setMessage("Some features of this app require a camera to operate. " +
                    "Those features will be disabled on this device.")
                    .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            dialogInterface.cancel();
                        }
                    });
            cmbnull.create().show();

        }

        d = new DecimalFormat("##");
        DataCollectionHandler dataCollectionHandler = new DataCollectionHandler(this);

}





    private void setButtons() {
        fbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(MainActivity.this, new String[] {Manifest.permission.CAMERA}, 1);

                }
                else {
                    if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                        fbutton.setTouch(true);
                        fbutton.invalidate();
                        if (manager.getBackStackEntryCount() > 0) {
                            manager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE);
                        }
                        if (activfragment.length() > 0) {
                            if (activfragment.equals("qs") == true) {
                                Fragment fg = manager.findFragmentById(R.id.fragment);
                                manager.beginTransaction().remove(fg).commit();
                                FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, new CamActivity());
                                ft.commit();
                                qbutton.setTouch(false);
                                qbutton.invalidate();
                                activfragment = "cam";
                                resetMeter();
                                cbutton.setClickable(false);

                            } else {

                                Fragment ft = manager.findFragmentById(R.id.fragment);
                                manager.beginTransaction().remove(ft).commit();
                                fbutton.setTouch(false);
                                fbutton.invalidate();
                                activfragment = "";
                                if (cbutton.checkTouch() == true) {
                                    cbutton.setTouch(false);
                                    cbutton.invalidate();
                                }
                                resetMeter();
                                cbutton.setClickable(true);
                            }
                        } else {
                            FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, new CamActivity());
                            ft.commit();
                            activfragment = "cam";
                            resetMeter();
                            cbutton.setClickable(false);
                        }
                    }
                    else {
                        fbutton.setTouch(false);
                        fbutton.invalidate();
                        if (ActivityCompat.shouldShowRequestPermissionRationale(MainActivity.this, Manifest.permission.CAMERA) == false) {
                            AlertDialog.Builder cmbnull = new AlertDialog.Builder(MainActivity.this);
                            cmbnull.setTitle("Permission Not Granted").setMessage("This feature requires camera. Required permission" +
                                    " was not granted. If you want to revert this permission refer to your device manual or device manufacturer.")
                                    .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                        @Override
                                        public void onClick(DialogInterface dialogInterface, int i) {

                                            dialogInterface.cancel();
                                        }
                                    });
                            cmbnull.create().show();
                        }
                        else {
                            ActivityCompat.requestPermissions(MainActivity.this, new String[] {Manifest.permission.CAMERA}, 1);

                        }
                    }
                }
            }
            });

        qbutton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    qbutton.setTouch(true);
                    if (manager.getBackStackEntryCount() > 0) {
                        manager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE);
                    }
                    if (activfragment.length() > 0) {
                        if (activfragment.equals("cam") == true) {
                            Fragment fg = manager.findFragmentById(R.id.fragment);
                            manager.beginTransaction().remove(fg).commit();
                            FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, new QsActivity());
                            ft.commit();
                            fbutton.setTouch(false);
                            fbutton.invalidate();
                            activfragment = "qs";
                            resetMeter();
                            cbutton.setClickable(false);

                        } else {
                            Fragment ft = manager.findFragmentById(R.id.fragment);
                            manager.beginTransaction().remove(ft).commit();
                            qbutton.setTouch(false);
                            if (cbutton.checkTouch() == true) {
                                cbutton.setTouch(false);
                                cbutton.invalidate();
                            }
                            activfragment = "";
                            resetMeter();
                            cbutton.setClickable(true);
                        }
                    }
                    else {
                        FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, new QsActivity());
                        ft.commit();
                        activfragment = "qs";
                        resetMeter();
                        cbutton.setClickable(false);
                    }

                }


        });

        cbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                cbutton.setTouch(true);
                if (manager.getBackStackEntryCount() > 0) {
                    manager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE);
                }
                if (testchk.equals("cam") == true) {
                    FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, qsActivity.newInstance(_id));
                    ft.commit();
                    qbutton.setTouch(true);
                    qbutton.invalidate();
                    activfragment = "qs";
                    resetMeter();
                    cbutton.setClickable(false);
                }
                else if (testchk.equals("qs") == true) {
                    if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(MainActivity.this, new String[] {Manifest.permission.CAMERA}, 1);

                    } else {
                        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                            FragmentTransaction ft = manager.beginTransaction().add(R.id.fragment, camActivity.newInstance(_id));
                            ft.commit();
                            fbutton.setTouch(true);
                            fbutton.invalidate();
                            activfragment = "cam";
                            resetMeter();
                            cbutton.setClickable(false);
                        } else {
                            if (ActivityCompat.shouldShowRequestPermissionRationale(MainActivity.this, Manifest.permission.CAMERA) == false) {
                                AlertDialog.Builder cmbnull = new AlertDialog.Builder(MainActivity.this);
                                cmbnull.setTitle("Permission Not Granted").setMessage("This feature requires camera. Required permission" +
                                        " was not granted. If you want to revert this permission refer to your device manual or manufacturer.")
                                        .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                            @Override
                                            public void onClick(DialogInterface dialogInterface, int i) {
                                                cbutton.setTouch(false);
                                                cbutton.invalidate();
                                                dialogInterface.cancel();
                                            }
                                        });
                                cmbnull.create().show();
                            }
                            else {
                                cbutton.setTouch(false);
                                cbutton.invalidate();
                                ActivityCompat.requestPermissions(MainActivity.this, new String[] {Manifest.permission.CAMERA}, 1);

                            }
                        }
                    }
                }
                else {
                    AlertDialog.Builder cmbnull = new AlertDialog.Builder(MainActivity.this);
                    cmbnull.setTitle("Insufficient Data").setMessage("This option combines the result of one test with the other. " +
                            "Please select \"F\" or \"Q\" to do a test first. If you have done a combined test then start a new test.")
                            .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            cbutton.setTouch(false);
                            cbutton.invalidate();
                            dialogInterface.cancel();
                        }
                    });
                    cmbnull.create().show();
                }
            }
        });

        rbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                rbutton.setTouch(true);
                List<Fragment> fragmentList = manager.getFragments();
                if (fragmentList.size() > 0) {
                    for (int i = 0; i < fragmentList.size(); i++) {
                        Fragment fg = fragmentList.get(i);
                        manager.beginTransaction().remove(fg).commit();
                    }

                    if (manager.getBackStackEntryCount() > 0) {
                        manager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE);
                    }
                }
                recreate();
            }
        });

    }

    private void resetMeter() {
        fullMeter.lightArc(false, -130);
        fullMeter.invalidate();
        mtext.setText(false, -130);
        mtext.invalidate();
        mtextin.setText("");
        pointer.setDegrees(-130);
        pointer.invalidate();
        if (isresponselit == true) {
            resetResponse();
        }
        percent.setText("");
    }

    private void camTest(double fwhr) {
            mfwhr = fwhr;
            float rotation = (float) (fwhrCalc(fwhr) * 260);
            rotation = -130 + rotation;
            int duration = (int) (fwhrCalc(fwhr) * 3000);
            final float maxval = rotation;
            PropertyValuesHolder holder = PropertyValuesHolder.ofFloat("degrees", -130, rotation);
            ValueAnimator animator = new ValueAnimator();
            animator.setDuration(duration);
            animator.setValues(holder);
            animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
                @Override
                public void onAnimationUpdate(ValueAnimator valueAnimator) {
                    Float degreeval = (float) valueAnimator.getAnimatedValue("degrees");
                    fullMeter.lightArc(true, degreeval);
                    fullMeter.invalidate();
                    pointer.setDegrees(degreeval);
                    pointer.invalidate();
                    percent.setText(d.format(((degreeval + 130) / 260) * 100) + "%");
                    percent.invalidate();
                    if (degreeval == maxval) {
                        mtext.setText(true, maxval);
                        mtext.invalidate();
                        setMeterText(degreeval);
                        getResponse(_id, "cam");
                    }

                }
            });
            animator.start();
            animator.setRepeatCount(0);
            testchk = "cam";
            cbutton.setClickable(true);

    }

    private double fwhrCalc(double fwhr) {
        double topadj = 1.91 - 1.65;
        double bottomadj = 1.65 - 1.45;
        fwhr = fwhr - 1.65;
        if (fwhr > 0) {
            fwhr = (fwhr / topadj) + 0.50;
            if (fwhr > 1) {
                fwhr = 1;
            }
        }
        else {
            fwhr = 0.50 + (fwhr / bottomadj);
            if (fwhr < 0) {
                fwhr = 0.05;
            }
        }

        return fwhr;
    }

    private void qsTest(double intn) {
        mintn = intn;
        float rotation = (float) (intn * 260);
        rotation = -130 + rotation;
        int duration = (int) (intn * 3000);
        final float maxval = rotation;
        PropertyValuesHolder holder = PropertyValuesHolder.ofFloat("degrees", -130, rotation);
        ValueAnimator animator = new ValueAnimator();
        animator.setDuration(duration);
        animator.setValues(holder);
        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator valueAnimator) {
                Float degreeval = (float) valueAnimator.getAnimatedValue("degrees");
                fullMeter.lightArc(true, (float) valueAnimator.getAnimatedValue("degrees"));
                fullMeter.invalidate();
                pointer.setDegrees((float) valueAnimator.getAnimatedValue("degrees"));
                pointer.invalidate();
                percent.setText(d.format(((degreeval + 130) / 260) * 100) + "%");
                percent.invalidate();
                if (degreeval == maxval) {
                    mtext.setText(true, maxval);
                    mtext.invalidate();
                    setMeterText(degreeval);
                    getResponse(_id, "qs");
                }

            }
        });
        animator.start();
        animator.setRepeatCount(0);
        testchk = "qs";
        cbutton.setClickable(true);
    }

    private void cmbnTest(double fwhr, double intn) {
        float rotation = (float) (((0.5 * fwhrCalc(fwhr)) + (0.5 * intn)) * 260);
        rotation = -130 + rotation;
        int duration = (int) (((0.5 * fwhrCalc(fwhr)) + (0.5 * intn)) * 3000);
        final float maxval = rotation;
        PropertyValuesHolder holder = PropertyValuesHolder.ofFloat("degrees", -130, rotation);
        ValueAnimator animator = new ValueAnimator();
        animator.setDuration(duration);
        animator.setValues(holder);
        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator valueAnimator) {
                Float degreeval = (float) valueAnimator.getAnimatedValue("degrees");
                fullMeter.lightArc(true, degreeval);
                fullMeter.invalidate();
                pointer.setDegrees(degreeval);
                pointer.invalidate();
                percent.setText(d.format(((degreeval + 130) / 260) * 100) + "%");
                percent.invalidate();
                if ((float) valueAnimator.getAnimatedValue("degrees") == maxval) {
                    mtext.setText(true, maxval);
                    mtext.invalidate();
                    setMeterText(degreeval);
                    getResponse(_id, "both");
                }

            }
        });
        animator.start();
        animator.setRepeatCount(0);
        testchk = "";
        _id = Integer.MIN_VALUE;
        cbutton.setClickable(true);
    }

    private void getResponse(final int _id, final String test) {
        isresponselit = true;
        rsptext.setLit(true);
        rsptext.invalidate();
        ybtn.setClick(true);
        ybtn.invalidate();
        ybtn.setClickable(true);
        nbtn.setClick(true);
        nbtn.invalidate();
        nbtn.setClickable(true);

        ybtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (test.equals("cam") == true) {
                    maindb.updateCamOutRecord(_id, "Y");
                }
                else if (test.equals("qs") == true) {
                    maindb.updateQsOutRecord(_id, "Y");

                }
                else {
                    maindb.updateQsOutRecord(_id, "Y");
                    maindb.updateCamOutRecord(_id, "Y");
                }
                resetResponse();
                Toast.makeText(MainActivity.this, "Thank you for your response", Toast.LENGTH_SHORT).show();

            }
        });

        nbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (test.equals("cam") == true) {
                    maindb.updateCamOutRecord(_id, "N");
                }
                else if (test.equals("qs") == true) {
                    maindb.updateQsOutRecord(_id, "N");

                }
                else {
                    maindb.updateQsOutRecord(_id, "N");
                    maindb.updateCamOutRecord(_id, "N");
                }
                resetResponse();
                Toast.makeText(MainActivity.this, "Thank you for your response", Toast.LENGTH_SHORT).show();
            }
        });

    }

    private void setMeterText(float angle) {
        if (-130 < angle && angle <= -78) {
            mtextin.setText("NO BULL");

        } else if (-78 < angle && angle <= -26) {
            mtextin.setText("U DAWG!");

        } else if (-26 < angle && angle <= 26) {
            mtextin.setText("UH OH!");

        } else if (26 < angle && angle <= 78) {
            mtextin.setText("HOLD YOUR HORSES");

        } else if (78 < angle && angle <= 130) {
            mtextin.setText("THE BEAST IS UNLEASHED");

        }
    }

    private void resetResponse() {
        rsptext.setLit(false);
        rsptext.invalidate();
        ybtn.setClick(false);
        ybtn.invalidate();
        ybtn.setClickable(false);
        nbtn.setClick(false);
        nbtn.invalidate();
        nbtn.setClickable(false);
        isresponselit = false;

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        for (int i = 0; i < menu.size(); i++) {
            Drawable iconcolor = menu.getItem(i).getIcon();
            iconcolor.mutate();
            iconcolor.setColorFilter(getResources().getColor(R.color.white), PorterDuff.Mode.SRC_IN);
        }
      return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.info) {
            MainActivity.this.finish();
            Intent intent = new Intent(MainActivity.this, HelpInfo.class);
            startActivity(intent);
            return true;
        }

        if (id == R.id.settings) {
            MainActivity.this.finish();
            Intent intent = new Intent(MainActivity.this, Settings.class);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);

    }

    @Override
    public void onRequestPermissionsResult(int requestcode, String permissions[], int[] grantresult) {
        if (requestcode == 1) {
            if (grantresult.length > 0 && grantresult[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(MainActivity.this, "Thank you. Enjoy!", Toast.LENGTH_SHORT).show();
            }

        }
    }

    @Override
    public void onFragmentInteraction(double fwhr, int dbid, boolean combinetest) {
    if (dbid != Integer.MIN_VALUE) {
        _id = dbid;
    }
    if (fwhr == 0) {

            Fragment ft = manager.findFragmentById(R.id.fragment);
            manager.beginTransaction().remove(ft).commit();
            activfragment = "";
            fbutton.setTouch(false);
            fbutton.invalidate();
            if (cbutton.checkTouch() == true) {
                cbutton.setTouch(false);
                cbutton.invalidate();
            }
            cbutton.setClickable(true);

        }
        else {
            if (combinetest == false) {
                Fragment ft = manager.findFragmentById(R.id.fragment);
                manager.beginTransaction().remove(ft).commit();
                activfragment = "";
                fbutton.setTouch(false);
                fbutton.invalidate();
                camTest(fwhr);
            }
            else {
                Fragment ft = manager.findFragmentById(R.id.fragment);
                manager.beginTransaction().remove(ft).commit();
                activfragment = "";
                fbutton.setTouch(false);
                fbutton.invalidate();
                cbutton.setTouch(false);
                cbutton.invalidate();
                cmbnTest(fwhr, mintn);
            }
        }
    }


    @Override
    public void onQsFragmentInteraction(double intn, int dbid, boolean combinetest) {
        if (dbid != Integer.MIN_VALUE) {
            _id = dbid;
        }
       if (intn == 0) {
            Fragment ft = manager.findFragmentById(R.id.fragment);
            manager.beginTransaction().remove(ft).commit();
            activfragment = "";
            qbutton.setTouch(false);
            qbutton.invalidate();
            if (cbutton.checkTouch() == true) {
                cbutton.setTouch(false);
                cbutton.invalidate();
            }
            cbutton.setClickable(true);
        }
        else {
            if (combinetest == false) {
                Fragment ft = manager.findFragmentById(R.id.fragment);
                manager.beginTransaction().remove(ft).commit();
                activfragment = "";
                qbutton.setTouch(false);
                qbutton.invalidate();
                qsTest(intn);
            }
            else {
                Fragment ft = manager.findFragmentById(R.id.fragment);
                manager.beginTransaction().remove(ft).commit();
                activfragment = "";
                qbutton.setTouch(false);
                qbutton.invalidate();
                cbutton.setTouch(false);
                cbutton.invalidate();
                cmbnTest(mfwhr, intn);
            }
        }
    }

    @Override
    public void onPause() {
        super.onPause();


    }

    @Override
    public void onResume() {
        super.onResume();


    }



}
