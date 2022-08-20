package com.smudge.cheat_o_meter;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.drawable.Drawable;
import android.hardware.Camera;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.FaceDetector;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.os.Process;
import android.preference.PreferenceManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;



import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.InputStream;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link CamActivity.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link CamActivity#newInstance} factory method to
 * create an instance of this fragment.
 */

//Fragment to load camera view and process the captured image results.


public class CamActivity extends Fragment implements CameraBridgeViewBase.CvCameraViewListener2, DetectionListener, Runnable {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String P_DBID = "dbid";
    private View fragmentview;
    private ImageButton capture, flipcam, zoomin, zoomout, flash;
    private Drawable capcolor;
    private Drawable flashcolor;
    private TextView caminfo;
    private List<ImageButton> btnclrlist = new ArrayList<ImageButton>();
    private RelativeLayout mainlayout;
    private CamLayout rectlayout;
    private JavaCameraView cvcam;
    private double zoomvalue = 1;
    private int cvcamid = CameraBridgeViewBase.CAMERA_ID_BACK;
    private boolean running = false;
    private Context cntxt;
    private List<String[]> extdata = new ArrayList<String[]>();
    private BaseLoaderCallback callback = new BaseLoaderCallback(cntxt) {
        @Override
        public void onManagerConnected(int status) {
            if (status == BaseLoaderCallback.SUCCESS) {
                cvcam.enableView();
                try {
                    loadCascadeFile();
                }
                catch (Throwable t) {
                    t.printStackTrace();
                }

            }
            else {
                super.onManagerConnected(status);
            }
        }
    };
    private CascadeClassifier cascadeClassifier;
    private CascadeClassifier eyecascade;
    private File cascadeFile;
    private File eyecascadeFile;
    private Mat faceimg;
    private Mat rotimg;
    private Mat resizeimg;
    private Mat flipimg;
    private MatOfRect matOfRect;
    private List<org.opencv.core.Rect> faceslist;
    private List<org.opencv.core.Rect> eyeslist;
    private boolean capturecmplt = false;
    private double xScale;
    private double yScale;
    private double rectadjx;
    private double rectadjy;
    private Size scale;
    private double fwhr = 0;
    private CollectedData camdb;
    private int _id;
    private boolean isflashon = false;
    private int pdbid = Integer.MIN_VALUE;
    private CustomTHandler dHandler;
    private SharedPreferences preferences;
    private int cammode = 0;
    // TODO: Rename and change types of parameters


    private OnFragmentInteractionListener mListener;

    public CamActivity() {
        // Required empty public constructor
    }

   public static CamActivity newInstance(int dbid) {

        CamActivity fragment = new CamActivity();
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
        fragmentview = inflater.inflate(R.layout.fragment_cam, container, false);
        mainlayout = (RelativeLayout) fragmentview.findViewById(R.id.mainlayout);
        rectlayout = (CamLayout) fragmentview.findViewById(R.id.rectlayout);
        capture = (ImageButton) fragmentview.findViewById(R.id.capture);
        capcolor = capture.getBackground();
        capcolor.mutate();
        flipcam = (ImageButton) fragmentview.findViewById(R.id.flipcam);
        zoomin = (ImageButton) fragmentview.findViewById(R.id.zoomin);
        flash = (ImageButton) fragmentview.findViewById(R.id.flash);
        flashcolor = flash.getBackground();
        flashcolor.mutate();
        zoomout = (ImageButton) fragmentview.findViewById(R.id.zoomout);
        btnclrlist.add(capture);
        btnclrlist.add(flash);
        btnclrlist.add(flipcam);
        btnclrlist.add(zoomin);
        btnclrlist.add(zoomout);
        for (int i = 0; i < btnclrlist.size(); i++) {
            Drawable btn = btnclrlist.get(i).getBackground();
            btn.mutate();
            if (i == 0) {
                capcolor.setColorFilter(getResources().getColor(R.color.beastL), PorterDuff.Mode.SRC_IN);
            }
            else if (i == 1) {
                btn.setColorFilter(getResources().getColor(R.color.white), PorterDuff.Mode.SRC_IN);
            }
            else {
                btn.setColorFilter(getResources().getColor(R.color.blue), PorterDuff.Mode.SRC_IN);
                }
            }
        caminfo = fragmentview.findViewById(R.id.caminfo);
        caminfo.setTextColor(Color.RED);
        cvcam = fragmentview.findViewById(R.id.layout);
        cvcam.setCameraIndex(cvcamid);
        cvcam.setVisibility(SurfaceView.VISIBLE);
        cvcam.setCvCameraViewListener(this);
        FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) mainlayout.getLayoutParams();
        params.width = getResources().getDisplayMetrics().widthPixels - 50;
        params.height = getResources().getDisplayMetrics().heightPixels / 2;
        params.topMargin = 50 / 2;
        xScale = params.width;
        yScale = params.height;
        mainlayout.setLayoutParams(params);
        rectlayout.bringToFront();
        flipcam.setRotationX(50);

        return fragmentview;
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        cntxt = getActivity();

        mListener = (OnFragmentInteractionListener) cntxt;
        camdb = new CollectedData(cntxt);
        camdb.open();
        Capture();
        FlipCam();
        ZoomIn();
        Flash();
        ZoomOut();
        preferences = PreferenceManager.getDefaultSharedPreferences(getActivity());
        if (preferences.contains("CamMode") == true) {
            if (preferences.getInt("CamMode", 0) == 0) {
                dHandler = new CustomTHandler("Face Detect", Process.THREAD_PRIORITY_DEFAULT);
                dHandler.start();
                dHandler.setListener(this);
                dHandler.setReceiver(ReceiverHandler());
            }
            else {
                cammode = 1;
            }
        }



       }


    @Override
    public void onResume() {
        super.onResume();
        if (OpenCVLoader.initDebug() == true) {
            callback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        } else {
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION, cntxt, callback);
        }
        cascadeClassifier = new CascadeClassifier(cascadeFile.getAbsolutePath());
        cascadeClassifier.load(cascadeFile.getAbsolutePath());
        eyecascade = new CascadeClassifier(eyecascadeFile.getAbsolutePath());
        eyecascade.load(cascadeFile.getAbsolutePath());
        if (cammode == 1){
                startDetection();
            }


        }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
         if (context instanceof OnFragmentInteractionListener) {
            mListener = (OnFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        if (cvcam != null) {
            cvcam.disableView();
        }
        if (camdb != null) {
            camdb.close();
            camdb = null;
        }
       mListener = null;
        if (dHandler != null) {
            dHandler.quit();
            dHandler.interrupt();
        }
        running = false;
        }

    private void loadCascadeFile() throws Throwable {
        File cascadedir = getActivity().getDir("haarcascade_frontalface_alt", Context.MODE_PRIVATE);
        cascadeFile = new File(cascadedir, "haarcascade_frontalface_alt.xml");
        File eyecascadedir = getActivity().getDir("haarcascade_eye", Context.MODE_PRIVATE);
        eyecascadeFile = new File(eyecascadedir, "haarcascade_eye.xml");

        if (cascadeFile.exists() == false) {
            FileOutputStream os = new FileOutputStream(cascadeFile);
            InputStream is = getResources().openRawResource(R.raw.haarcascade_frontalface_alt);
            byte[] buffer = new byte[4096];
            int bytesread;
            while ((bytesread = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesread);
            }
            is.close();
            os.close();
        }

        if (eyecascadeFile.exists() == false) {
            FileOutputStream os = new FileOutputStream(eyecascadeFile);
            InputStream is = getResources().openRawResource(R.raw.haarcascade_eye);
            byte[] buffer = new byte[4096];
            int bytesread;
            while ((bytesread = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesread);
            }
            is.close();
            os.close();
        }

    }

    private Handler ReceiverHandler() {
        Handler handler;
        handler = new Handler(Looper.getMainLooper()) {
                @Override
                public void handleMessage(Message inputmsg) {
                    super.handleMessage(inputmsg);
                   }
            };

        return handler;
    }

    private void Capture() {
        capture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               if (capturecmplt == true) {
                           capturecmplt = false;
                           if (pdbid == Integer.MIN_VALUE) {
                               camdb.createRecord("", "", String.valueOf(fwhr), "");
                               Cursor cursor = camdb.callAllRecord();
                               if (cursor.getCount() > 0) {
                                   cursor.moveToLast();
                                   _id = cursor.getInt(0);
                               }
                               mListener.onFragmentInteraction(fwhr, _id, false);
                           }
                           else {
                               camdb.updateCamInRecord(pdbid, String.valueOf(fwhr));
                               mListener.onFragmentInteraction(fwhr, Integer.MIN_VALUE, true);
                           }

                       }
                       else {
                           AlertDialog.Builder capture = new AlertDialog.Builder(cntxt);
                           capture.setTitle("Capture Incomplete").setMessage("Face capture is not complete. Do you want to proceed?").
                                   setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                                       @Override
                                       public void onClick(DialogInterface dialogInterface, int i) {
                                           mListener.onFragmentInteraction(fwhr, Integer.MIN_VALUE, false);

                                       }
                                   })
                                   .setNegativeButton("No", new DialogInterface.OnClickListener() {
                                       @Override
                                       public void onClick(DialogInterface dialogInterface, int i) {
                                           dialogInterface.cancel();
                                       }
                                   });
                           capture.create().show();
                       }



            }
        });
    }

    private void FlipCam() {
        flipcam.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                caminfo.setText("");
                if (cvcamid == CameraBridgeViewBase.CAMERA_ID_BACK) {
                    if (cntxt.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA_FRONT) == true) {
                        cvcam.disableView();
                        cvcamid = CameraBridgeViewBase.CAMERA_ID_FRONT;
                        cvcam.setCameraIndex(cvcamid);
                        cvcam.enableView();
                        Camera.Parameters parameters = cvcam.getCamInstance().getParameters();
                        if (parameters.getMaxNumDetectedFaces() < 0) {
                            caminfo.setText("This hardware does not support face detection.");
                        }
                    }
                    else {
                        AlertDialog.Builder capture = new AlertDialog.Builder(cntxt);
                        capture.setTitle("Front Camera Not Found").setMessage("Front camera was not found on your device.").
                                setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialogInterface, int i) {
                                        dialogInterface.cancel();

                                    }
                                });
                        capture.create().show();
                    }
                }
                else if (cvcamid == CameraBridgeViewBase.CAMERA_ID_FRONT) {
                    cvcam.disableView();
                    cvcamid = CameraBridgeViewBase.CAMERA_ID_BACK;
                    cvcam.setCameraIndex(cvcamid);
                    cvcam.enableView();
                   Camera.Parameters parameters = cvcam.getCamInstance().getParameters();
                   if (parameters.getMaxNumDetectedFaces() < 0) {
                       caminfo.setText("This hardware does not support face detection.");
                   }
                }

            }
        });
    }



private boolean checkFlash(int camid) {
        Camera.Parameters parameters = cvcam.getCamInstance().getParameters();
        boolean hasFlash = false;
        List<String> flashmode = parameters.getSupportedFlashModes();

        if (flashmode != null) {
            if (flashmode.contains(parameters.FLASH_MODE_TORCH) == true) {
                hasFlash = true;
            } else {
                hasFlash = false;
            }
        }
            else {
                hasFlash = false;
            }

            return hasFlash;
        }



    private void ZoomIn() {
        zoomin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (zoomvalue == 1) {
                    zoomvalue = 1.25;
                }
                else if (zoomvalue > 1 && zoomvalue < 2.25) {
                    zoomvalue += 0.25;
                }
                else {
                    zoomvalue = 2.25;
                }
            }
        });
    }

    private void Flash() {
        flash.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkFlash(cvcamid) == true) {

                     if (isflashon == false){
                        isflashon = true;
                        flashcolor.setColorFilter(getResources().getColor(R.color.yellow), PorterDuff.Mode.SRC_IN);
                        cvcam.disableView();
                        cvcam.setFlashToggle(true);
                        cvcam.enableView();
                        }
                    else {
                        isflashon = false;
                        flashcolor.setColorFilter(getResources().getColor(R.color.white), PorterDuff.Mode.SRC_IN);
                        cvcam.disableView();
                        cvcam.setFlashToggle(false);
                        cvcam.enableView();

                    }

                }
                else {
                    AlertDialog.Builder capture = new AlertDialog.Builder(cntxt);
                    capture.setTitle("Flash Not Supported").setMessage("Flash is not available on device or the appropriate flash " +
                            "mode is not supported.").
                            setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialogInterface, int i) {
                                    dialogInterface.cancel();

                                }
                            });
                    capture.create().show();
                }
            }
        });
    }

    private void ZoomOut() {
        zoomout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (zoomvalue > 1) {
                    zoomvalue -= 0.25;
                }
                else {
                    zoomvalue = 1;
                }
            }
        });
    }

    @Override
    public void onCameraViewStarted(int width, int height) {

    }

    @Override
    public void onCameraViewStopped() {
        }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
       cvcam.setScale(zoomvalue);
   if (faceimg == null) {
       faceimg = inputFrame.gray();
       if (cammode == 0) {
           dHandler.detectFace(faceimg, cvcamid, xScale, yScale, zoomvalue, cascadeClassifier, eyecascade);
       }
   }
        return inputFrame.rgba();

    }

    @Override
    public void FaceDetected(org.opencv.core.Rect rect, double adjx, double adjy) {
    if (cammode == 0) {
        if (rect != null) {
            rectlayout.setFace(rect, adjx, adjy);
            rectlayout.invalidate();

        } else {
            rectlayout.invalidate();
            faceimg = null;
        }
    }
    }

    @Override
    public void EyesDetected(org.opencv.core.Rect facerect, org.opencv.core.Rect eyesrect) {
        if (cammode == 0) {
            if (eyesrect != null) {
                rectlayout.setEyes(eyesrect);
                rectlayout.invalidate();
                capcolor.setColorFilter(cntxt.getResources().getColor(R.color.green), PorterDuff.Mode.SRC_IN);
                fwhr = (double) ((eyesrect.br().x - eyesrect.tl().x))
                        / ((facerect.br().y - facerect.tl().y) / 2);
                capturecmplt = true;
                faceimg = null;


            } else {
                rectlayout.invalidate();
                capcolor.setColorFilter(cntxt.getResources().getColor(R.color.beastL), PorterDuff.Mode.SRC_IN);
                capturecmplt = false;
                faceimg = null;
            }
        }
    }

    private void startDetection() {
        new Thread(this).start();
    }

    @Override
    public void run() {
        running = true;
        while (running == true) {
            try {
                if (faceimg != null) {
                    rotimg = new Mat();
                    if (cvcamid == CameraBridgeViewBase.CAMERA_ID_BACK) {
                        Core.rotate(faceimg, rotimg, Core.ROTATE_90_CLOCKWISE);
                    } else {
                        Core.rotate(faceimg, rotimg, Core.ROTATE_90_COUNTERCLOCKWISE);
                    }
                    Size scale = new Size(xScale * zoomvalue, yScale * zoomvalue);
                    resizeimg = new Mat();
                    Imgproc.resize(rotimg, resizeimg, scale);
                    rectadjx = (resizeimg.width() - xScale) / 2;
                    rectadjy = (resizeimg.height() - yScale) / 2;
                    flipimg = new Mat();
                    if (cvcamid == CameraBridgeViewBase.CAMERA_ID_FRONT) {
                        Core.flip(resizeimg, flipimg, 1);
                    } else {
                        flipimg = resizeimg;
                    }
                    MatOfRect matOfRect = new MatOfRect();
                    cascadeClassifier.detectMultiScale(flipimg, matOfRect);
                    faceslist = matOfRect.toList();
                    if (faceslist.size() > 0) {
                        getActivity().runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                rectlayout.setFace(faceslist.get(0), rectadjx, rectadjy);
                                rectlayout.invalidate();
                            }
                        });

                        Mat eyeimg = flipimg.submat(faceslist.get(0));
                        MatOfRect eyerect = new MatOfRect();
                        eyecascade.detectMultiScale(eyeimg, eyerect);
                        eyeslist = eyerect.toList();
                        if (eyeslist.size() > 0) {
                            getActivity().runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    rectlayout.setEyes(eyeslist.get(0));
                                    rectlayout.invalidate();
                                    capcolor.setColorFilter(cntxt.getResources().getColor(R.color.green), PorterDuff.Mode.SRC_IN);
                                }
                            });

                            fwhr = (double) ((eyeslist.get(0).br().x - eyeslist.get(0).tl().x))
                                    / ((faceslist.get(0).br().y - faceslist.get(0).tl().y) / 2);
                            capturecmplt = true;

                        }
                        else {
                            getActivity().runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    capcolor.setColorFilter(cntxt.getResources().getColor(R.color.beastL), PorterDuff.Mode.SRC_IN);
                                }
                            });
                            capturecmplt = false;
                        }

                    }

                }

                faceimg = null;
            }
            catch (Exception e) {

            }

        }

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
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(double fwhr, int dbid, boolean combinetest);

    }



}
