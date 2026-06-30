import type { Meta, StoryObj } from "@storybook/react";
import { Heatmap } from "./Heatmap";

const meta: Meta<typeof Heatmap> = { title: "Charts/Heatmap", component: Heatmap };
export default meta;
type Story = StoryObj<typeof Heatmap>;

const cell = (v: number, owned = false) => ({
  value: v,
  text: v >= 0.5 ? `+${v.toFixed(0)}` : v > -0.5 ? "·" : v.toFixed(0),
  owned,
});

export const LockLift: Story = {
  args: {
    cols: ["CursTot", "Drannith", "RuleLaw", "Linvala", "OppAgent"],
    rows: [
      { label: "Radiation Sickness · 70%", cells: [cell(-1), cell(-1), cell(-1), cell(-2), cell(-2)] },
      { label: "The Genome Project · 67%", cells: [cell(3), cell(3), cell(3), cell(2), cell(2)] },
      { label: "Kefka · 42%", cells: [cell(3, true), cell(6), cell(5), cell(3), cell(3)] },
      { label: "Zero-Sum Game · 33%", cells: [cell(6), cell(7), cell(6), cell(5), cell(4)] },
      { label: "Crystal Sickness · 9%", cells: [cell(4), cell(4), cell(4), cell(3), cell(2)] },
    ],
  },
};
