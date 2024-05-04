import { expect, test, describe, beforeAll } from "vitest";
import { mount } from '@vue/test-utils'
import CommentList from "@/components/CommentList.vue";
import { Comment, CommentMeta } from "@/components/types";


describe("CommentList.vue", () => {
  test("renders comment list", () => {
    const comments: Comment[] = [
      {
        id: 1,
        parent: null,
        user: "User1",
        date: "2023-05-26",
        comment: "Hello World",
      },
      {
        id: 2,
        parent: 1,
        user: "User2",
        date: "2023-05-27",
        comment: "Hello back",
      },
    ];

    const commentMeta: CommentMeta = {
      content_type: "cast.post",
      object_pk: "1",
      timestamp: "1685519465",
      security_hash: "fea323148dc8d5886db3e30c1f4714f35b130073",
      csrfToken: "ELgJPDvW24T0u7NGr4i9z8nyKIFNThd4Y6PNyPUEhKv1N5CMAPdQxrk2IF5mYdKL",
      postCommentUrl: new URL("http://localhost:8000/show/comments/post/ajax/"),
    }

    expect(CommentList).toBeTruthy()

    const wrapper = mount(CommentList, {
      props: {
        comments: comments,
        commentMeta,
      },
    })

    expect(wrapper.findAllComponents({ name: "CommentItem" })).toHaveLength(2);
  });
});
