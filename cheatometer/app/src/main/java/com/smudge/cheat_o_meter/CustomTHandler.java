package com.smudge.cheat_o_meter;

import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.os.Message;
import android.util.Log;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Rect;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.util.List;

public class CustomTHandler extends HandlerThread {

    private Handler handler;
    private Handler rechandler;
    private Runnable task;
    private Mat rotimg;
    private Mat resizeimg;
    private Mat flipimg;
    private double rectadjx = 0;
    private double rectadjy = 0;
    private CascadeClassifier eyecascade;
    public static final int FACE_SUCCESS = 2;
    public static final int FACE_FAILURE = -2;
    public static final int EYE_SUCCESS = 3;
    public static final int EYE_FAILURE = -3;
    private String logtag = "Handler Thread";
    private DetectionListener detectionListener;
    private Rect srect;
    private Rect[] srectarr;

    public CustomTHandler(String name) {
        super(name);
        }

    public CustomTHandler(String name, int priority) {
        super(name, priority);
      }

    public void setListener(DetectionListener listener) {
        this.detectionListener = listener;
    }

    public void setReceiver(Handler handler) {
        this.rechandler = handler;
    }

    @Override
    protected void onLooperPrepared() {
        super.onLooperPrepared();
        handler = new Handler(getLooper(), new Handler.Callback() {
            @Override
            public boolean handleMessage(Message inputmsg) {
                if (inputmsg.obj instanceof Rect) {
                    srect = (Rect) inputmsg.obj;
                }
                else {
                    srectarr = (Rect[]) inputmsg.obj;
                }

                switch (inputmsg.what) {
                    case FACE_SUCCESS:
                       rechandler.post(new Runnable() {
                            @Override
                            public void run() {
                                detectionListener.FaceDetected(srect, rectadjx, rectadjy);
                            }
                        });
                         break;

                    case EYE_SUCCESS:
                        rechandler.post(new Runnable() {
                            @Override
                            public void run() {
                                detectionListener.EyesDetected(srectarr[0], srectarr[1]);
                            }
                        });
                        break;

                    case FACE_FAILURE:
                        rechandler.post(new Runnable() {
                            @Override
                            public void run() {
                           detectionListener.FaceDetected(null, rectadjx, rectadjy);
                            }
                        });
                        break;

                    case EYE_FAILURE:
                        rechandler.post(new Runnable() {
                            @Override
                            public void run() {
                                detectionListener.EyesDetected(null, null);
                            }
                        });
                        break;

                        default:
                        break;
                }
                return true;
            }


        });
    }

   public void detectFace(Mat faceimg, int cvcamid, double xScale, double yScale, double zoom, CascadeClassifier facecascade,
                           CascadeClassifier eyecascade) {

            rotimg = new Mat();
            if (cvcamid == CameraBridgeViewBase.CAMERA_ID_BACK) {
                Core.rotate(faceimg, rotimg, Core.ROTATE_90_CLOCKWISE);
            } else {
                Core.rotate(faceimg, rotimg, Core.ROTATE_90_COUNTERCLOCKWISE);
            }
            Size scale = new Size(xScale * zoom, yScale * zoom);
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
            facecascade.detectMultiScale(flipimg, matOfRect);
            List<Rect> faceslist = matOfRect.toList();
            if (faceslist.size() > 0) {
                synchronized (handler) {
                    handleState(faceslist.get(0), null, FACE_SUCCESS);
                }
                Mat eyeimg = flipimg.submat(faceslist.get(0));
                MatOfRect eyerect = new MatOfRect();
                eyecascade.detectMultiScale(eyeimg, eyerect);
                List<Rect> eyeslist = eyerect.toList();
                if (eyeslist.size() > 0) {
                    Rect[] rectarr = new Rect[] {faceslist.get(0), eyeslist.get(0)};
                    synchronized (handler) {
                        handleState(null, rectarr, EYE_SUCCESS);
                    }
                }
                else {
                    synchronized (handler) {
                        handleState(null, null, EYE_FAILURE);
                    }
                }

            }
            else {
                synchronized (handler) {
                    handleState(null, null, FACE_FAILURE);
                }
            }
        }



    public void handleState(Rect rect, Rect[] rectarr, int state) {
        if (state == EYE_SUCCESS) {
            Message message = handler.obtainMessage(state, rectarr);
            message.sendToTarget();
        }
        else {
            Message message = handler.obtainMessage(state, rect);
            message.sendToTarget();
        }

    }

}
