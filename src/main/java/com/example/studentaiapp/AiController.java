package com.example.studentaiapp;

import com.example.studentaiapp.service.AiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.util.Map;
import java.io.IOException;

@RequestMapping("/api/ai")
@RestController
public class AiController {

    private final AiService aiService;

    @Autowired
    public AiController(AiService aiService) {
        this.aiService = aiService;
    }

    @PostMapping("/api/ask")
    public ResponseEntity<String> ask(@RequestBody Map<String, String> body) throws IOException {
        String prompt = body.get("prompt");
        String response = aiService.getAnswerFromLocalAi(prompt);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/api/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) throws IOException {
        String response = aiService.processFile(file);
        return ResponseEntity.ok(response);
    }
}

