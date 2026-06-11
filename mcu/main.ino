void setup() {
  Serial.begin(115200);
  Serial.println("ESP32_READY");
}

void loop() {
  if (Serial.available()) {

    String objectType = Serial.readStringUntil('\n');
    objectType.trim();

    processAiDecision(objectType);
  }
}

void processAiDecision(String objectType) {

  Serial.print("Received: ");
  Serial.println(objectType);

  if (objectType == "bottle") {
    Serial.println("CMD: ACTUATE_BIN_1");
  }

  else if (objectType == "cup") {
    Serial.println("CMD: ACTUATE_BIN_2");
  }

  else if (objectType == "book") {
    Serial.println("CMD: ACTUATE_BIN_3");
  }

  else {
    Serial.println("ERR: UNKNOWN_OBJECT_TYPE");
  }
}