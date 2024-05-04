import { expect, test, describe } from "vitest";
import CommentItem from "@/components/CommentItem.vue";
import { Comment } from "@/components/types";
import { mount } from '@vue/test-utils'

describe("CommentItem.vue", () => {
  test("renders comment item", async () => {
    const comment: Comment = {
      id: 1,
      parent: null,
      user: "User1",
      date: "2023-05-26",
      comment: "Hello World",
    };

    const comments: Comment[] = [
      comment,
      {
        id: 2,
        parent: 1,
        user: "User2",
        date: "2023-05-27",
        comment: "Hello back",
      },
    ];

    expect(CommentItem).toBeTruthy()

    const wrapper = mount(CommentItem, {
      props: {
        comment: comment,
        comments: comments,
      },
    })

    expect(wrapper.text()).toContain("User1");
    expect(wrapper.text()).toContain("Hello World");
    expect(wrapper.findAllComponents({ name: "CommentItem" })).toHaveLength(1);
  })

  test("shows reply form when reply button is clicked", async () => {
    const comment: Comment = {
      id: 1,
      parent: null,
      user: "User1",
      date: "2023-05-26",
      comment: "Hello World",
    };
    const comments: Comment[] = [comment];

    const wrapper = mount(CommentItem, {
      props: {
        comment: comment,
        comments: comments,
        commentsEnabled: true,
      },
    })

    expect(wrapper.vm.showReplyForm).toBe(false);
    await wrapper.find("button").trigger("click");
    expect(wrapper.vm.showReplyForm).toBe(true);
  });
});
