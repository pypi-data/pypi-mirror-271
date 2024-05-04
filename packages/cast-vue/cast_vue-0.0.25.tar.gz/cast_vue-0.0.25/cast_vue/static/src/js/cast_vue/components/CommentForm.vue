<template>
    <div class="comment-form">
      <div class="input-field">
        <label for="fname">Name: </label>
        <input id="fname" type="text" v-model="comment.name" placeholder="Your name">
      </div>
      <div class="input-field">
        <label for="femail">Mail Address: </label>
        <input id="femail" type="text" v-model="comment.email" placeholder="Your email">
      </div>
      <div class="input-field">
        <label for="ftitle">Title: </label>
        <input id="ftitle" type="text" v-model="comment.title" placeholder="Title">
      </div>
      <div class="input-field">
        <textarea v-model="comment.comment" placeholder="Add a comment..."></textarea>
      </div>
      <div class="input-field">
        <button @click="submitComment" :disabled="!isFormValid" class="submit-button">Submit</button>
      </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, reactive, PropType, computed } from 'vue';
import { CommentInputData } from './types';

export default defineComponent({
    props: {
        parent: {
            type: Number as PropType<number>,
            required: false,
        },
    },
    emits: ["comment-submitted"],
    setup(props, context) {
        let parent = null;
        if (props.parent) {
            parent = props.parent.toString();
        }
        const comment = reactive({parent: parent, comment: "", name: "", email: "", title: ""} as CommentInputData)

        const submitComment = () => {
            console.log('Submit new comment:', comment.comment);
            context.emit("comment-submitted", comment);
            comment.comment = "";
        };

        const isFormValid = computed(() => comment.name !== '' && comment.comment !== '');

        return {
            comment,
            isFormValid,
            submitComment,

        }
    }
});
</script>
<style scoped>
.comment-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

.input-field {
  margin-bottom: 20px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button.submit-button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
