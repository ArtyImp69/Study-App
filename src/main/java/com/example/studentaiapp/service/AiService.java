package com.example.studentaiapp.service;

import okhttp3.*;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Objects;
import okhttp3.*;
import org.json.JSONObject;

@Service
public class AiService {

    private final OkHttpClient client = new OkHttpClient(); // ✅ qui la variabile globale

    public String processText(String inputText) throws IOException {
        RequestBody body = RequestBody.create(
                inputText,
                MediaType.get("text/plain; charset=utf-8")
        );

        Request request = new Request.Builder()
                .url("http://localhost:8000/api/generate")
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) throw new IOException("Errore nella richiesta: " + response);
            return Objects.requireNonNull(response.body()).string();
        }
    }

    public String getAnswerFromLocalAi(String prompt) throws IOException {
        JSONObject json = new JSONObject();
        json.put("prompt", prompt);

        RequestBody body = RequestBody.create(
                json.toString(),
                MediaType.get("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
                .url("http://localhost:8000/api/generate")
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected code " + response);
            }
            String responseBody = response.body().string();
            JSONObject jsonResponse = new JSONObject(responseBody);
            return jsonResponse.getString("answer");
        }
    }

    public String processFile(MultipartFile file) throws IOException {
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", file.getOriginalFilename(),
                        RequestBody.create(file.getBytes(), MediaType.parse(file.getContentType())))
                .build();

        Request request = new Request.Builder()
                .url("http://localhost:5000/api/process-file")
                .post(requestBody)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) throw new IOException("Errore nella richiesta file: " + response);
            return Objects.requireNonNull(response.body()).string();
        }
    }
}
