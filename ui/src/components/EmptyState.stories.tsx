import type { Meta, StoryObj } from "@storybook/react";
import { EmptyState } from "./EmptyState";

const meta: Meta<typeof EmptyState> = { title: "EmptyState", component: EmptyState };
export default meta;
type Story = StoryObj<typeof EmptyState>;

export const Championship: Story = {
  args: {
    glyph: "🏆",
    title: "No tournament run yet",
    children: "Set the trials and T_grind, then press Run to seed 16 decks, play 4 group pods, and crown a champion.",
  },
};

export const Locks: Story = {
  args: {
    glyph: "🔒",
    title: "No lock sweep run yet",
    children: "Press Run lock sweep to measure what each persistent lock buys each deck vs the pod.",
  },
};
