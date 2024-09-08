<template>
  <div class="container">
    <h1>Testing Instructions Generator</h1>

    <!-- Optional Context Input -->
    <div class="form-group">
      <label for="context">Context (Optional):</label>
      <textarea v-model="context" class="form-control" placeholder="Enter context here..." id="context" rows="3"></textarea>
    </div>

    <!-- Multi Image Uploader -->
    <div class="form-group">
      <label for="screenshots" class="form-label">Upload Screenshots (Required):</label>
      <input class="form-control" type="file" id="screenshots" multiple @change="handleImageUpload" />
    </div>

    <!-- Button to describe testing instructions -->
    <div class="form-group">
      <button class="btn btn-primary" :disabled="!files.length" @click="describeTestingInstructions">
        Describe Testing Instructions
      </button>
    </div>

    <!-- Preview of Uploaded Images -->
    <div v-if="images.length" class="image-preview">
      <h3>Uploaded Images:</h3>
      <div class="images-container">
        <img v-for="(image, index) in images" :key="index" :src="image" alt="Screenshot" />
      </div>
    </div>

    <!-- Displaying Test Instructions -->
    <div v-if="testCases.length" class="test-instructions">
      <h3>Generated Testing Instructions:</h3>
      <div v-for="(testCase, index) in testCases" :key="index" class="test-case">
        <h4>{{ index + 1 }}. {{ testCase.Description }}</h4>
        <p><strong>Pre-conditions:</strong> {{ testCase.preConditions }}</p>
        <p><strong>Testing Steps:</strong></p>
        <ul>
          <li v-for="(step, stepIndex) in testCase.steps" :key="stepIndex">{{ step }}</li>
        </ul>
        <p><strong>Expected Result:</strong> {{ testCase.expectedResult }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      context: '',
      images: [],     // Array to hold image previews (base64)
      files: [],      // Array to hold file objects (for FormData)
      testCases: []   // Holds the test instructions from the backend
    };
  },
  methods: {
    handleImageUpload(event) {
      this.files = Array.from(event.target.files); // Store file objects for FormData

      // Generate base64 previews for the images
      this.images = [];
      for (let i = 0; i < this.files.length; i++) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.images.push(e.target.result);
        };
        reader.readAsDataURL(this.files[i]);
      }
    },
    async describeTestingInstructions() {
      const formData = new FormData();
      formData.append('context', this.context);

      // Append images to the form data
      this.files.forEach((file) => {
        formData.append('screenshots', file);
      });

      try {
        // Send a POST request to the Flask backend
        const response = await fetch('http://127.0.0.1:5000/describe', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Error in API call');
        }

        const data = await response.json();

        // Transform keys with spaces into valid object keys
        this.testCases = data.test_cases.map((testCase) => {
          return {
            Description: testCase.Description,
            preConditions: testCase["Pre-conditions"],   // Transform key
            steps: testCase["Testing Steps"],            // Transform key
            expectedResult: testCase["Expected Result"]  // Transform key
          };
        });
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate testing instructions.');
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.image-preview {
  margin-top: 20px;
}

.images-container {
  display: flex;
  flex-wrap: wrap;
}

.images-container img {
  width: 100px;
  height: 100px;
  margin: 5px;
  object-fit: cover;
  border: 1px solid #ccc;
  border-radius: 12px;
}

.test-instructions {
  margin-top: 20px;
}

.test-case {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-case h4 {
  margin-bottom: 10px;
}
</style>
