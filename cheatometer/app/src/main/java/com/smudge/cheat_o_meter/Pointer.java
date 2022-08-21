package com.smudge.cheat_o_meter;


import android.animation.PropertyValuesHolder;
import android.animation.ValueAnimator;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;

public class Pointer extends View {

    private Bitmap pointer;
    private Rect rect;
    private float adjustment;
    private float rotation = -130;

    public Pointer(Context context) {
        super(context);
        init();
    }

    public Pointer(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public Pointer(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        pointer = BitmapFactory.decodeResource(getResources(), R.mipmap.pointertall_fg);
        pointer = Bitmap.createBitmap(pointer);
        rect = new Rect();


    }

   public void setDegrees(float degrees) {
        this.rotation = degrees;
    }

    @Override
    public void onMeasure(int width, int height) {
        int w = getResources().getDisplayMetrics().widthPixels;
        int h = getResources().getDisplayMetrics().heightPixels;
        int rectleft = pointer.getWidth() + pointer.getWidth();
        int rectbottom = pointer.getHeight() + pointer.getHeight();
        rect.set(0, 0, rectleft, rectbottom);
        adjustment = pointer.getHeight()/4;
        rect.offsetTo(w / 2 - (rect.width() / 2), h / 4 + (50 / 2) - (rect.height() / 2) - (int) adjustment);

        setMeasuredDimension(w, w);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float xr = rect.exactCenterX();
        float yr = rect.exactCenterY();
        canvas.save();
        canvas.rotate(rotation, xr, yr + adjustment);
        canvas.drawBitmap(pointer, null, rect, null);

    }


}
