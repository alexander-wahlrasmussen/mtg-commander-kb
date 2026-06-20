import type { Meta, StoryObj } from "@storybook/react";
import { BracketPod } from "./BracketPod";

const meta: Meta<typeof BracketPod> = { title: "BracketPod", component: BracketPod };
export default meta;
type Story = StoryObj<typeof BracketPod>;

export const GroupPod: Story = {
  args: {
    title: "Pod A",
    hint: "win share",
    seats: [
      { name: "The Genome Project", seed: 1, share: 0.42, advances: true },
      { name: "The Replication Crisis", seed: 8, share: 0.31 },
      { name: "The Dark Lord's Army", seed: 9, share: 0.16 },
      { name: "The Grand Design", seed: 16, share: 0.11 },
    ],
  },
};

export const FinalFour: Story = {
  args: {
    final: true,
    title: "The Final Four",
    hint: "group winners",
    seats: [
      { name: "The Genome Project", seed: 1, share: 0.41, medal: "gold" },
      { name: "Zero-Sum Game", seed: 5, share: 0.27, medal: "silver" },
      { name: "Radiation Sickness", seed: 3, share: 0.19, medal: "bronze" },
      { name: "The Exile's Return", seed: 4, share: 0.13 },
    ],
  },
};
