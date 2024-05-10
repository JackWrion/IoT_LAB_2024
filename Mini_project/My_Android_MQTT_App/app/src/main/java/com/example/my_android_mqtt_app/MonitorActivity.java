package com.example.my_android_mqtt_app;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;


import com.google.android.material.card.MaterialCardView;
import com.google.android.material.slider.LabelFormatter;
import com.google.android.material.slider.Slider;
import com.google.android.material.switchmaterial.SwitchMaterial;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;


import java.nio.charset.StandardCharsets;

public class MonitorActivity extends AppCompatActivity {

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_monitor);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main_monitor), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });


        //---------------------------------------------------------//
        // -------------------INIT COMPONENT-----------------------//
        //---------------------------------------------------------//
        SwitchMaterial ledSw = findViewById(R.id.SwitchLED);
        TextView TextPower = findViewById(R.id.TextPowerLED);
        ImageView imgLED = findViewById(R.id.imageLED);
        TextView TitleLed = findViewById(R.id.TitleLED);
        imgLED.setColorFilter(getColor(R.color.default500));
        ledSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // isChecked will be true if the switch is checked, false otherwise
                if (isChecked) {
                    TextPower.setTextColor(getColor(R.color.ledyellow2));
                    TitleLed.setTextColor(getColor(R.color.ledyellow2));
                    //imgLED.setColorFilter(getColor(R.color.ledyellow2));
                    imgLED.setColorFilter(getColor(R.color.ledyellow2));
                    imgLED.setElevation(50);
                    //ledCard.setCardBackgroundColor(getColor(R.color.amber));
                    MQTTHelper.myStaticMQTT.sendDataMQTT("jackwr/feeds/led", "1");
                } else {
                    //ledCard.setCardBackgroundColor(getColor(com.google.android.material.R.color.m3_sys_color_dynamic_light_surface_container_low ));
                    TextPower.setTextColor(getColor(R.color.default500));
                    TitleLed.setTextColor(getColor(R.color.default500));
                    imgLED.setImageResource(R.drawable.light_off);
                    imgLED.setColorFilter(getColor(R.color.default500));
                    imgLED.setElevation(0);
                    MQTTHelper.myStaticMQTT.sendDataMQTT("jackwr/feeds/led", "0");
                }
            }
        });





        SwitchMaterial heaterSw = findViewById(R.id.SwitchHeater);
        ImageView imgHeater = findViewById(R.id.imageHeater);
        TextView TitleHeater = findViewById(R.id.TitleHeater);
        imgHeater.setColorFilter(getColor(R.color.default500));
        heaterSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // isChecked will be true if the switch is checked, false otherwise
                if (isChecked) {
                    TitleHeater.setTextColor(getColor(R.color.heater_red));
                    imgHeater.setColorFilter(getColor(R.color.heater_red));
                    imgHeater.setElevation(50);
                    //ledCard.setCardBackgroundColor(getColor(R.color.amber));
                    MQTTHelper.myStaticMQTT.sendDataMQTT("jackwr/feeds/water-heater", "1");
                } else {
                    //ledCard.setCardBackgroundColor(getColor(com.google.android.material.R.color.m3_sys_color_dynamic_light_surface_container_low ));
                    TitleHeater.setTextColor(getColor(R.color.default500));
                    imgHeater.setColorFilter(getColor(R.color.default500));
                    imgHeater.setElevation(0);
                    MQTTHelper.myStaticMQTT.sendDataMQTT("jackwr/feeds/water-heater", "0");
                }
            }
        });





        Slider sliderAir = findViewById(R.id.SliderAir);
        ImageView imgAir = findViewById(R.id.air_condition_img);
        TextView titleAir = findViewById(R.id.TitleAirCon);
        imgAir.setColorFilter(getColor(R.color.bright_blue));
        sliderAir.addOnSliderTouchListener(new Slider.OnSliderTouchListener() {
            @Override
            public void onStartTrackingTouch(@NonNull Slider slider) {
                titleAir.setShadowLayer(10, 0, 0, getColor(R.color.cyan));
                imgAir.setElevation(50);
                imgAir.setOutlineAmbientShadowColor(getColor(R.color.cyan));
            }

            @Override
            public void onStopTrackingTouch(@NonNull Slider slider) {
                titleAir.setShadowLayer(0, 0, 0, getColor(R.color.cyan));
                int data = (int)sliderAir.getValue();
                MQTTHelper.myStaticMQTT.sendDataMQTT("jackwr/feeds/air-conditioner", Integer.toString(data));
            }
        });




        ImageView tempImg = findViewById(R.id.imageTemper);
        tempImg.setColorFilter(getColor(R.color.terra_cotta));
        TextView tempTxt = findViewById(R.id.TextTemperature);

        ImageView humidImg = findViewById(R.id.imageHumi);
        humidImg.setColorFilter(getColor(R.color.teal));
        TextView humidTxt = findViewById(R.id.TextHumi);

        ImageView batterImg = findViewById(R.id.imageBattery);
        batterImg.setColorFilter(getColor(R.color.battery_color));
        TextView batteryTxt = findViewById(R.id.TextBattery);




        MQTTHelper myMQTT = MQTTHelper.GetMQTTClient(this);
        myMQTT.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                Toast.makeText(MonitorActivity.this, "MQTT CONNECTION COMPLETE...", Toast.LENGTH_SHORT).show();
            }
            @Override
            public void connectionLost(Throwable cause) {
                Toast.makeText(MonitorActivity.this, (CharSequence) cause, Toast.LENGTH_SHORT).show();
                myMQTT.connect();
            }
            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {

                if (topic.contains("air")){
                    int data = Integer.parseInt(message.toString());
                    sliderAir.setValue(data);
                }
                else if (topic.contains("led")){
                    int data = Integer.parseInt(message.toString());
                    ledSw.setChecked(data != 0);
                }
                else if (topic.contains("heater")){
                    int data = Integer.parseInt(message.toString());
                    heaterSw.setChecked(data != 0);
                }
                else if (topic.contains("temp")){
                    String data = message.toString();
                    data = data + " °C";
                    tempTxt.setText(data);
                }
                else if (topic.contains("humi")){
                    String data = message.toString();
                    data = data + " ‰";
                    humidTxt.setText(data);
                }
                else if (topic.contains("battery")){
                    String data = message.toString();
                    data = data + " kWh";
                    batteryTxt.setText(data);
                }
                Log.d("MQTT","GET DATA: " + topic + " --->  " + message.toString());
            }
            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
//
//
//        sliderAir.setOnTouchListener(new View.OnTouchListener() {
//            @Override
//            public boolean onTouch(View v, MotionEvent event) {
//
//
//                //titleAir.setShadowLayer(10, 0, 0, getColor(R.color.cyan));
//
//
////                if (event.getAction() == MotionEvent.ACTION_UP) {// Handle touch up event
////                    titleAir.setShadowLayer(0, 0, 0, getColor(R.color.cyan));
////                    imgAir.setElevation(0);
////                    imgAir.setOutlineAmbientShadowColor(getColor(R.color.cyan));
////                }
////                else {
////
////                }
////                // Return true to indicate that the event has been consumed
//                return true;
//
//            }
//        });









    }




}