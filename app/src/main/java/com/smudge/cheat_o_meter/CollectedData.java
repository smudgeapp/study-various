package com.smudge.cheat_o_meter;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.ContactsContract;

public class CollectedData {

private static final String DATABASE_MAIN = "maindatabase";
private static final int DATABASE_VERSION = 1;

private static final String KEY_ID = "id";
private static final String KEY_INPUT = "input";
private static final String KEY_OUT = "output";
private static final String KEY_CAMIN = "caminput";
private static final String KEY_CAMOUT = "camout";

private static final String DATABASE_CREATE= "create table " + DATABASE_MAIN + " (" +
         KEY_ID + " integer primary key autoincrement," + KEY_INPUT + " text," +
         KEY_OUT + " text," + KEY_CAMIN + " text," + KEY_CAMOUT + " text)";


private SQLiteDatabase maindb;
private DBHelper helper;
private final Context context;

public CollectedData(Context cntxt) {
    this.context = cntxt;
}

public CollectedData open() throws SQLException  {
    helper = new DBHelper(context);
    maindb = helper.getWritableDatabase();
    return this;
}

public void close() {
    helper.close();
}

public long createRecord(String qinput, String qoutput, String caminput, String camout) {
    ContentValues values = new ContentValues();
    values.put(KEY_INPUT, qinput);
    values.put(KEY_OUT, qoutput);
    values.put(KEY_CAMIN, caminput);
    values.put(KEY_CAMOUT, camout);

    return maindb.insert(DATABASE_MAIN, null, values);
}

public boolean deleteRecord(String id) {
    return maindb.delete(DATABASE_MAIN, KEY_ID + "=" + id, null) > 0;
}

public boolean deleteAllRecord() {
    return maindb.delete(DATABASE_MAIN, null, null) > 0;
}

public Cursor callAllRecord() {
    return maindb.query(DATABASE_MAIN, new String[] {KEY_ID, KEY_INPUT, KEY_OUT, KEY_CAMIN, KEY_CAMOUT}, null, null,
            null, null, null);
}

public boolean updateRecord(long id, String qinput, String qoutput, String camin, String camout) {
    ContentValues values = new ContentValues();
    values.put(KEY_INPUT, qinput);
    values.put(KEY_OUT, qoutput);
    values.put(KEY_CAMIN, camin);
    values.put(KEY_CAMOUT, camout);

    return maindb.update(DATABASE_MAIN, values, KEY_ID + "=" + id, null) > 0;
}

public boolean updateQsInRecord(long id, String qinput) {
    ContentValues values = new ContentValues();
    values.put(KEY_INPUT, qinput);

    return maindb.update(DATABASE_MAIN, values, KEY_ID + "=" + id, null) > 0;
}

    public boolean updateQsOutRecord(long id, String qoutput) {
        ContentValues values = new ContentValues();
        values.put(KEY_OUT, qoutput);

        return maindb.update(DATABASE_MAIN, values, KEY_ID + "=" + id, null) > 0;
    }

    public boolean updateCamInRecord(long id, String camin) {
        ContentValues values = new ContentValues();
        values.put(KEY_CAMIN, camin);

        return maindb.update(DATABASE_MAIN, values, KEY_ID + "=" + id, null) > 0;
    }

    public boolean updateCamOutRecord(long id, String camout) {
        ContentValues values = new ContentValues();
        values.put(KEY_CAMOUT, camout);

        return maindb.update(DATABASE_MAIN, values, KEY_ID + "=" + id, null) > 0;
    }



public static class DBHelper extends SQLiteOpenHelper {
    DBHelper(Context cntx) {
        super(cntx, DATABASE_MAIN, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase sqLiteDatabase) {
        sqLiteDatabase.execSQL(DATABASE_CREATE);

    }

    @Override
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i1) {

    }
}



}
