import * as z from "zod";

export const ratingCreateSchema = z.object({
  rated_user_username: z
    .string()
    .trim()
    .min(1, { message: "A technician must be selected" }),
  rating: z
    .number()
    .min(1, { message: "Rating must be at least 1" })
    .max(5, { message: "Rating cannot be more than 5" }),
  comment: z
    .string()
    .min(1, { message: "Tell us more about your rating" })
    .max(500, { message: "Comment must be 500 characters or fewer" }),
});

export type TRatingCreateSchema = z.infer<typeof ratingCreateSchema>;