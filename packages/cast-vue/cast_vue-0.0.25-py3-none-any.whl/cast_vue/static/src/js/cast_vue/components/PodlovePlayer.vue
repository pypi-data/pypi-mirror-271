<template>
    <div ref="player"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount, ref } from 'vue';
declare const podlovePlayer: any;


export default defineComponent({
    name: 'PodlovePlayer',
    props: {
        elementId: {
            type: String,
            required: true,
        },
        apiUrl: {
            type: String,
            required: true,
        },
        playerConfig: {
            type: URL,
            required: true,
        },
    },
    setup(props) {
        const player = ref(null);

        onMounted(() => {
            // Ensure that the function is available globally
            if (typeof podlovePlayer === 'function') {
                podlovePlayer(props.elementId, props.apiUrl, props.playerConfig);
            }
        });

        onBeforeUnmount(() => {
            // Perform any necessary cleanup here
        });

        return { player };
    },
});
</script>
