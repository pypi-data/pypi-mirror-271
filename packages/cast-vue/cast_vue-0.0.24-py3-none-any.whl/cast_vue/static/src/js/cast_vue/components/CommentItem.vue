<template>
    <div class="comment">
        <div class="comment-user">{{ comment.user }}</div>
        <div class="comment-date">{{ comment.date }}</div>
        <div class="comment-body">{{ comment.comment }}</div>
        <div v-if="commentsEnabled">
            <button @click="showReplyForm = !showReplyForm">Reply</button>
            <div v-if="showReplyForm">
                <comment-form :parent="comment.id" @comment-submitted="submitReply"></comment-form>
            </div>
        </div>
        <div class="comment-children" v-if="hasChildren">
            <div v-for="child in children" :key="child.id">
                <comment-item :comment="child" :comments="comments" :comments-enabled="commentsEnabled"/>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, reactive } from 'vue';
import { Comment, CommentInputData } from './types';
import CommentForm from './CommentForm.vue';

export default defineComponent({
    name: 'CommentItem',
    components: {
        CommentForm,
    },
    props: {
        comment: {
            type: Object as PropType<Comment>,
            required: true,
        },
        comments: {
            type: Array as PropType<Comment[]>,
            required: true,
        },
        commentsEnabled: {
            type: Boolean as PropType<boolean>,
            required: true,
        },
    },
    emits: ['comment-submitted'],
    setup(props, context) {
        const reply = reactive({parent: props.comment.id.toString(), comment: "", name: "", email: "", title: ""} as CommentInputData);
        const showReplyForm = ref(false);
        const children = computed(() =>
            props.comments.filter((c) => c.parent === props.comment.id)
        );
        const hasChildren = computed(() => children.value.length > 0);

        const submitReply = (comment: CommentInputData) => {
            showReplyForm.value = false;
            context.emit('comment-submitted', comment);
        };

        return {
            reply,
            showReplyForm,
            submitReply,
            children,
            hasChildren,
        };
    },
});
</script>
<style scoped>
.comment {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
}

.comment-children {
    margin-top: 10px;
}

.comment-user {
    font-weight: bold;
}

.comment-date {
    color: #888;
    font-size: 0.8em;
}

.comment-children {
    margin-left: 20px;
}
</style>
