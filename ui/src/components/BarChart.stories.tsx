import type { Meta, StoryObj } from "@storybook/react";
import { BarChart } from "./BarChart";

const meta: Meta<typeof BarChart> = { title: "Charts/BarChart", component: BarChart };
export default meta;
type Story = StoryObj<typeof BarChart>;

const rows = [
  { label: "Radiation Sickness", values: { win: 69, pure: 57 } },
  { label: "The Genome Project", values: { win: 66, pure: 65 } },
  { label: "The Replication Crisis", values: { win: 59, pure: 43 } },
  { label: "The Exile's Return", values: { win: 45, pure: 35 } },
  { label: "Lightning War", values: { win: 34, pure: 12 } },
  { label: "The Grand Design", values: { win: 24, pure: 8 } },
];

export const Default: Story = {
  args: {
    rows,
    series: [
      { key: "win", label: "P(WIN)", color: "#5cd2ff" },
      { key: "pure", label: "PURE RACE", color: "#ffb454" },
    ],
    height: 360,
  },
};
