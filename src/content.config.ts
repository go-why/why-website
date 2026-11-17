import { defineCollection, z } from 'astro:content';

// Collection « docs » : les pages FR/EN vivent dans src/content/docs/{fr,en}/**.
// Frontmatter typé (title, weight) — weight ordonne la nav (comme Hugo).
const docs = defineCollection({
  schema: z.object({
    title: z.string(),
    weight: z.coerce.number().default(100),
  }),
});

export const collections = { docs };
