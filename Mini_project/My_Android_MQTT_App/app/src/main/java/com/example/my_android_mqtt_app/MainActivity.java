package com.example.my_android_mqtt_app;


import android.os.Handler;
import android.os.Looper;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.material.materialswitch.MaterialSwitch;
import com.google.android.material.progressindicator.BaseProgressIndicator;
import com.google.android.material.progressindicator.CircularProgressIndicator;
import com.google.android.material.progressindicator.LinearProgressIndicator;
import com.google.android.material.progressindicator.LinearProgressIndicatorSpec;
import com.google.android.material.switchmaterial.SwitchMaterial;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });


        Button btnHello = findViewById(R.id.Start_btn);
        btnHello.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                Toast.makeText(MainActivity.this, "Why you click too long", Toast.LENGTH_SHORT).show();
                return true;
            }
        });


        CircularProgressIndicator myProgress = findViewById(R.id.Progress_view);
        myProgress.setVisibility(View.INVISIBLE);
        btnHello.setOnClickListener(new View.OnClickListener() {
            @Override
            public synchronized void onClick(View v) {
                // Create a Handler to delay the start of MonitorActivity
                Intent intent = new Intent(MainActivity.this, MonitorActivity.class);

                myProgress.setVisibility(View.VISIBLE);

                MQTTHelper myMQTT = MQTTHelper.GetMQTTClient(MainActivity.this);

                startActivity(intent);
            }
        });



    }



}