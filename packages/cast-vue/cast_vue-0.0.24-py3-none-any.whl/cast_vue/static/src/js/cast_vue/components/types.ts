import { AnymatchFn } from "vite";
import { Comment } from "vue";

export interface Comment {
  id: number;
  parent: number | null;
  user: string;
  date: string;
  comment: string;
}

export interface CommentMeta {
  content_type: string;
  object_pk: string;
  timestamp: string;
  security_hash: string;
  postCommentUrl: URL;
  csrfToken: string;
  commentsAreEnabled: boolean;
}

export interface CommentResponse {
  success: boolean;
  action: string;
  errors: string;
  object_id: string;
  parent_id: string | null;
  comment_id: string;
  is_moderated: boolean;
  html: string;
  use_threadedcomments: boolean;
}

export interface CommentInputData {
  parent: string;
  comment: string;
  name: string;
  email: string;
  title: string;
}

export interface CommentFormData {
  [key: string]: string;
  content_type: string;
  object_pk: string;
  comment: string;
  name: string;
  email: string;
  title: string;
  security_hash: string;
  timestamp: string;
  parent: string;
}

export interface CommentSecurityData {
  content_type: string;
  object_pk: string;
  timestamp: string;
  security_hash: string;
}

export interface Post {
  id: number;
  title: string;
  visible_date: string;
  html_overview: string;
  html_detail: string;
  comments_are_enabled: boolean;
  comments: [Comment];
  comments_security_data: CommentSecurityData,
  podlove_players: [string, string][]; // [elementId, apiUrl]
  meta: {
    type: string;
    detail_url: string;
    html_url: string;
    slug: string;
    first_published_at: string;
  };
}

export interface PostsFromApi {
  meta: {
    total_count: number;
  };
  items: [Post];
}

export interface ModalSource {
  src: string;
  srcset: string;
  type: string;
  sizes: string;
}

export interface ModalImage {
  src: string;
  alt: string;
  srcset: string;
  sizes: string;
  height: string;
  width: string;
  next: string;
  prev: string;
}

export interface Form {
  search: string;
  date_after: string;
  date_before: string;
  date_facets: string;
  category_facets: string;
  tag_facets: string;
  order: string;
  page: number;
}

export interface ArticleData {
  articleDate: string;
  articleDateTime: string;
  articleAuthor: string;
}

interface Facet {
  slug: string;
  name: string;
  count: number;
}

export interface FacetCounts {
  date_facets: [Facet];
  category_facets: [Facet];
  tag_facets: [Facet];
}


export interface Theme {
  slug: string;
  name: string;
  selected: boolean;
}
