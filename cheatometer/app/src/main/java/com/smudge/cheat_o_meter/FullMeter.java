package com.smudge.cheat_o_meter;


import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.Shader;
import android.graphics.SweepGradient;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.util.TypedValue;
import android.view.View;
import android.view.WindowManager;

import java.util.ArrayList;
import java.util.List;

import static com.smudge.cheat_o_meter.SplashScreen.acth;

public class FullMeter extends View {

private RectF canvasrect;
private RectF arcrect;
private Paint arcpaint1, arcpaint2, arcpaint3, arcpaint4, arcpaint5;
private Paint arclight1, arclight2, arclight3, arclight4, arclight5;
private float angle;
private boolean light;
private List<Paint> arcpaints = new ArrayList<Paint>();
private Bitmap bgtexture;


    public FullMeter(Context context) {
        super(context);
        init();
    }

    public FullMeter(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public FullMeter(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        canvasrect = new RectF();
        arcrect = new RectF();

        arcpaint1 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arcpaint1.setStyle(Paint.Style.FILL);
        arcpaint1.setColor(getResources().getColor(R.color.nobull));
        arcpaint2 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arcpaint2.setStyle(Paint.Style.FILL);
        arcpaint2.setColor(getResources().getColor(R.color.dawg));
        arcpaint3 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arcpaint3.setStyle(Paint.Style.FILL);
        arcpaint3.setColor(getResources().getColor(R.color.uhoh));
        arcpaint4 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arcpaint4.setStyle(Paint.Style.FILL);
        arcpaint4.setColor(getResources().getColor(R.color.holdhorses));
        arcpaint5 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arcpaint5.setStyle(Paint.Style.FILL);
        arcpaint5.setColor(getResources().getColor(R.color.beast));
        arclight1 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight1.setStyle(Paint.Style.FILL);
        arclight1.setColor(getResources().getColor(R.color.nobullL));
        arclight2 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight2.setStyle(Paint.Style.FILL);
        arclight2.setColor(getResources().getColor(R.color.dawgL));
        arclight3 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight3.setStyle(Paint.Style.FILL);
        arclight3.setColor(getResources().getColor(R.color.uhohL));
        arclight4 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight4.setStyle(Paint.Style.FILL);
        arclight4.setColor(getResources().getColor(R.color.holdhorsesL));
        arclight5 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight5.setStyle(Paint.Style.FILL);
        arclight5.setColor(getResources().getColor(R.color.beastL));
        arcpaints.add(arcpaint1);
        arcpaints.add(arcpaint2);
        arcpaints.add(arcpaint3);
        arcpaints.add(arcpaint4);
        arcpaints.add(arcpaint5);


        bgtexture = BitmapFactory.decodeResource(getResources(), R.drawable.bgtexture1);


    }

    @Override
    public void onMeasure(int width, int height) {
        int w = getResources().getDisplayMetrics().widthPixels;
        int h = getResources().getDisplayMetrics().heightPixels;
        int ht = MeasureSpec.getSize(height);
        canvasrect.set(0,0, w, ht);
        float arcw = w - 50;
        float arch = h/2;
        arcrect.set(0, 0, arcw, arch);
        float arcxy = (w - arcw)/2;
        arcrect.offsetTo((int) arcxy, (int) arcxy);
        bgtexture = Bitmap.createScaledBitmap(bgtexture, w, ht, false);

        setMeasuredDimension(w, ht);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        canvas.drawBitmap(bgtexture, null, canvasrect, null);

        float startval = 140;
        for (int i = 0; i < 5; i++) {
            canvas.drawArc(arcrect, startval, 260/5, true, arcpaints.get(i));
            startval = startval + 260/5;
        }

        if (light == true) {

            if (-130 < angle && angle <= -78) {
                canvas.drawArc(arcrect, 140, 52, true, arclight1);
            } else if (-78 < angle && angle <= -26) {
                canvas.drawArc(arcrect, 192, 52, true, arclight2);
            } else if (-26 < angle && angle <= 26) {
                canvas.drawArc(arcrect, 244, 52, true, arclight3);
            } else if (26 < angle && angle <= 78) {
                canvas.drawArc(arcrect, 296, 52, true, arclight4);
            } else if (78 < angle && angle <= 130) {
                canvas.drawArc(arcrect, 348, 52, true, arclight5);
            }
        }


    }

    public void lightArc(boolean light, float angle) {
        this.angle = angle;
        this.light = light;

    }


}
