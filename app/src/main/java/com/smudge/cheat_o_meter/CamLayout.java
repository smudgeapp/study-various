package com.smudge.cheat_o_meter;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.hardware.Camera;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;

import java.util.List;

public class CamLayout extends View {

private Rect facerect;
private Paint facepaint;
private Paint chkpaint;
private Rect chkrect;
private Rect adjrect;
private List<org.opencv.core.Rect> rectList;


    public CamLayout(@NonNull Context context) {
        super(context);
        init();
    }

    public CamLayout(@NonNull Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public CamLayout(@NonNull Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        adjrect = new Rect();
        facerect = new Rect();
        facepaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        facepaint.setStyle(Paint.Style.STROKE);
        facepaint.setColor(getResources().getColor(R.color.nobullL));
        chkrect = new Rect();
        chkpaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        chkpaint.setStyle(Paint.Style.STROKE);
        chkpaint.setColor(getResources().getColor(R.color.dawgL));
    }

    @Override
    public void onMeasure(int w, int h) {
        int wt = getResources().getDisplayMetrics().widthPixels - 50;
        int ht = getResources().getDisplayMetrics().heightPixels / 2;
        adjrect.set(0, 0, wt, ht);
        setMeasuredDimension(wt, ht);

    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

      canvas.drawRect(facerect, facepaint);
      canvas.drawRect(chkrect, chkpaint);
    }




    public void setFace(org.opencv.core.Rect rectlist, double rectadjx, double rectadjy) {

        if (rectlist != null) {
                int x = (int) (rectlist.tl().x - rectadjx);
                int y = (int) (rectlist.tl().y - rectadjy);
                int wt = x + rectlist.width;
                int ht = y + rectlist.height;
                facerect.set(x, y, wt, ht);
            }
    }
    public void setEyes(org.opencv.core.Rect eyesrect) {
        if (eyesrect != null) {
            int x = (int) eyesrect.tl().x +  facerect.left;
            int y = (int) eyesrect.tl().y + facerect.top + (int) eyesrect.br().y / 4;
            int wt = (int) eyesrect.br().x + x;
            int ht = (int) eyesrect.br().y / 3 + y;
            chkrect.set(x, y, wt, ht);
        }
    }



}
