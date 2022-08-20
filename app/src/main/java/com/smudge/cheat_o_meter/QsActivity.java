package com.smudge.cheat_o_meter;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.RadioGroup;
import android.widget.RelativeLayout;
import android.widget.ScrollView;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link QsActivity.OnQsFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link QsActivity#newInstance} factory method to
 * create an instance of this fragment.
 */
public class QsActivity extends Fragment {
    private static final String P_DBID = "dbid";
    private View qsfragment;
    private RadioGroup q1radiogroup, q2radiogroup, q3radiogroup, q4radiogroup, q5radiogroup, q6radiogroup;
    private Button next;
    private ScrollView scrlayout;
    private int q1val = 0;
    private int q2val = 0;
    private int q3val = 0;
    private int q4val = 0;
    private int q5val = 0;
    private int q6val = 0;
    private CollectedData datadb;
    private String qinvalues = "";
    private Context context;
    private boolean valin = false;
    private Integer[] returnval = new Integer[6];
    private double intn = 0;
    private int _id;
    private int pdbid = Integer.MIN_VALUE;
    private OnQsFragmentInteractionListener mListener;

    public QsActivity() {
        // Required empty public constructor
    }

    public static QsActivity newInstance(int dbid) {
        QsActivity fragment = new QsActivity();
        Bundle args = new Bundle();
        args.putInt(P_DBID, dbid);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            pdbid = getArguments().getInt(P_DBID);

        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        qsfragment = inflater.inflate(R.layout.fragment_qs, container, false);
        q1radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q1radiogrp);
        q2radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q2radiogrp);
        q3radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q3radiogrp);
        q4radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q4radiogrp);
        q5radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q5radiogrp);
        q6radiogroup = (RadioGroup) qsfragment.findViewById(R.id.q6radiogrp);
        next = (Button) qsfragment.findViewById(R.id.next);
        next.setTextColor(Color.WHITE);
        scrlayout = (ScrollView) qsfragment.findViewById(R.id.scrlayout);
        FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) scrlayout.getLayoutParams();
        int w = getResources().getDisplayMetrics().widthPixels;
        int h = getResources().getDisplayMetrics().heightPixels;
        params.height = h / 2;
        params.width = w;
        params.topMargin = 50 / 2;
        scrlayout.setLayoutParams(params);
        scrlayout.setBackgroundColor(getResources().getColor(R.color.white));
        scrlayout.bringToFront();
        return qsfragment;
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        context = getActivity();
        datadb = new CollectedData(context);
        datadb.open();
        mListener = (OnQsFragmentInteractionListener) context;
        questionSelection();
        nextButton();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof OnQsFragmentInteractionListener) {
            mListener = (OnQsFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        if (datadb != null) {
            datadb.close();
            datadb = null;
        }
        mListener = null;
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnQsFragmentInteractionListener {
        // TODO: Update argument type and name
        void onQsFragmentInteraction(double intn, int dbid, boolean combinetest);
    }

    private void nextButton() {
        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                valStore();
                if (valin == true) {
                    if (pdbid == Integer.MIN_VALUE) {
                        Cursor cursor = datadb.callAllRecord();
                        if (cursor.getCount() > 0) {
                            cursor.moveToLast();
                        }
                        _id = cursor.getInt(0);
                        mListener.onQsFragmentInteraction(intn, _id, false);
                    }
                    else {
                        mListener.onQsFragmentInteraction(intn, Integer.MIN_VALUE, true);
                    }
                }
                else {
                    mListener.onQsFragmentInteraction(intn, Integer.MIN_VALUE, false);
                }
                qinvalues = "";

            }
        });

    }

    private void valCalc(Integer[] responses) {
        int a = responses[0] * responses[1];
        int sn = responses[2] * responses[3];
        int pbc = responses[4] * responses[5];
        intn = a + sn + pbc;
        if (intn == 0) {
            intn = 0.50;
        }
        else if (intn < 0){
            intn = (intn * -1) / 126;
        }
        else {
            intn = (intn + 63) / 126;
        }

    }

    private void valStore() {
        if (valin == true) {
            returnval = new Integer[]{q1val, q2val, q3val, q4val, q5val, q6val};
            valCalc(returnval);
            for (int i = 0; i < returnval.length; i++) {
                qinvalues += returnval[i];
                if (i < returnval.length - 1) {
                    qinvalues += "_,_";
                }

            }
            if (pdbid == Integer.MIN_VALUE) {
                datadb.createRecord(qinvalues, "", "", "");
            }
            else {
                datadb.updateQsInRecord(pdbid, qinvalues);
            }
        }
    }

    private void questionSelection() {
        q1radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q1val = optionSelection1(i);
                valin = true;

            }
        });

        q2radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q2val = optionSelection2(i);
                valin = true;
            }
        });

        q3radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q3val = optionSelection3(i);
                valin = true;
            }
        });

        q4radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q4val = optionSelection4(i);
                valin = true;
            }
        });

        q5radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q5val = optionSelection5(i);
                valin = true;
            }
        });

        q6radiogroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                q6val = optionSelection6(i);
                valin = true;
            }
        });

    }

    private int optionSelection1(int id) {
        int q1val = 0;

        switch (id) {
            case R.id.q1o1:
                q1val = 3;
                break;
            case R.id.q1o2:
                q1val = 2;
                break;
            case R.id.q1o3:
                q1val = 1;
                break;
            case R.id.q1o4:
                q1val = 0;
                break;
            case R.id.q1o5:
                q1val = -1;
                break;
            case R.id.q1o6:
                q1val = -2;
                break;
            case R.id.q1o7:
                q1val = -3;
                break;
            default:
                break;
        }

        return q1val;
    }

    private int optionSelection2(int id) {
        int q2val = 0;

        switch (id) {
            case R.id.q2o1:
                q2val = 7;
                break;
            case R.id.q2o2:
                q2val = 6;
                break;
            case R.id.q2o3:
                q2val = 5;
                break;
            case R.id.q2o4:
                q2val = 4;
                break;
            case R.id.q2o5:
                q2val = 3;
                break;
            case R.id.q2o6:
                q2val = 2;
                break;
            case R.id.q2o7:
                q2val = 1;
                break;
            default:
                break;
        }

        return q2val;
    }

    private int optionSelection3(int id) {
        int q3val = 0;

        switch (id) {
            case R.id.q3o1:
                q3val = -3;
                break;
            case R.id.q3o2:
                q3val = -2;
                break;
            case R.id.q3o3:
                q3val = -1;
                break;
            case R.id.q3o4:
                q3val = 0;
                break;
            case R.id.q3o5:
                q3val = 1;
                break;
            case R.id.q3o6:
                q3val = 2;
                break;
            case R.id.q3o7:
                q3val = 3;
                break;
            default:
                break;
        }

        return q3val;
    }

    private int optionSelection4(int id) {
        int q4val = 0;

        switch (id) {
            case R.id.q4o1:
                q4val = 1;
                break;
            case R.id.q4o2:
                q4val = 2;
                break;
            case R.id.q4o3:
                q4val = 3;
                break;
            case R.id.q4o4:
                q4val = 4;
                break;
            case R.id.q4o5:
                q4val = 5;
                break;
            case R.id.q4o6:
                q4val = 6;
                break;
            case R.id.q4o7:
                q4val = 7;
                break;
            default:
                break;
        }

        return q4val;
    }

    private int optionSelection5(int id) {
        int q5val = 0;

        switch (id) {
            case R.id.q5o1:
                q5val = -3;
                break;
            case R.id.q5o2:
                q5val = -2;
                break;
            case R.id.q5o3:
                q5val = -1;
                break;
            case R.id.q5o4:
                q5val = 0;
                break;
            case R.id.q5o5:
                q5val = 1;
                break;
            case R.id.q5o6:
                q5val = 2;
                break;
            case R.id.q5o7:
                q5val = 3;
                break;
            default:
                break;
        }

        return q5val;
    }

    private int optionSelection6(int id) {
        int q6val = 0;

        switch (id) {
            case R.id.q6o1:
                q6val = 1;
                break;
            case R.id.q6o2:
                q6val = 2;
                break;
            case R.id.q6o3:
                q6val = 3;
                break;
            case R.id.q6o4:
                q6val = 4;
                break;
            case R.id.q6o5:
                q6val = 5;
                break;
            case R.id.q6o6:
                q6val = 6;
                break;
            case R.id.q6o7:
                q6val = 7;
                break;
            default:
                break;
        }

        return q6val;
    }

}
