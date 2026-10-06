"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { formatDistanceToNow, parseISO } from "date-fns";
import { EyeIcon, MessageSquareQuoteIcon } from "lucide-react";
import {
  formatDate,
  getRepliesText,
  getViewText,
} from "@/utils";

type PostCardPost = {
  id: string;
  title: string;
  slug: string;
  body: string;
  created_at: string;
  updated_at: string;
  view_count: number;
  replies_count: number;
};

export default function PostCard({ post }: { post: PostCardPost }) {
  return (
    <Card className="dark:border-gray rounded-lg border">
      <CardHeader className="dark:text-platinum pb-4 w-full">
        <CardTitle className="font-robotoSlab text-center text-2xl">
          {post.title.length > 25
            ? `${post.title.substring(0, 25)}....`
            : post.title}
        </CardTitle>
        <CardDescription>
          <div className="flex flex-row justify-between">
            <div>
              <span>Posted on</span>
              <span className="dark:text-pumpkin ml-1">
                {formatDate(post.created_at).toString()}
              </span>
            </div>
          </div>
          <div>
            <span>Last Updated</span>
            <span className="dark:text-pumpkin ml-1">
              {formatDistanceToNow(parseISO(post.updated_at), {
                addSuffix: true,
              })}
            </span>
          </div>
        </CardDescription>
      </CardHeader>
      <CardContent className="border-t-deepBlueGrey dark:border-gray border-y py-4 text-sm">
        <p className="dark:text-platinum">
          {post.body.length > 65 ? `${post.body.substring(0, 65)}....` : post.body}
        </p>
      </CardContent>
      <div className="flex flex-row items-center justify-between p-2">
        <div>
          <Link href={`/post/${post.slug}`}>
            <Button size="sm" className="lime-gradient text-babyPowder">
              View Post
            </Button>
          </Link>
        </div>
        <div className="flex-row-center dark:text-platinum">
          <EyeIcon className="post-icon text-electricIndigo mr-1" />
          {getViewText(post.view_count)}
        </div>
        <div className="flex-row-center dark:text-platinum">
          <MessageSquareQuoteIcon className="post-icon text-electricIndigo mr-1" />
          <span>{getRepliesText(post.replies_count)}</span>
        </div>
      </div>
    </Card>
  );
}