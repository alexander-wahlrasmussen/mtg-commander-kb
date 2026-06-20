import type { Meta, StoryObj } from "@storybook/react";
import { ChampionBanner } from "./ChampionBanner";

const meta: Meta<typeof ChampionBanner> = { title: "ChampionBanner", component: ChampionBanner };
export default meta;
type Story = StoryObj<typeof ChampionBanner>;

export const Default: Story = {
  args: {
    name: "The Genome Project",
    seed: 1,
    note: "Runner-up: Zero-Sum Game (#5). ✨ Cinderella: The Exile's Return (#4).",
  },
};

export const Upset: Story = {
  args: {
    name: "Eldrazi Stampede Chaos",
    seed: 13,
    note: "Runner-up: The Genome Project (#1). ⚡ UPSET — the #13 seed took the crown.",
  },
};
