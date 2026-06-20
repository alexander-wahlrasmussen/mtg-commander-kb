import type { Meta, StoryObj } from "@storybook/react";
import { StatTable } from "./StatTable";
import type { Column } from "./StatTable";

const meta: Meta<typeof StatTable> = { title: "StatTable", component: StatTable };
export default meta;
type Story = StoryObj<typeof StatTable>;

interface Row {
  deck: string;
  sc: number;
  decap: string;
  pure: number;
  win: number;
}
const rows: Row[] = [
  { deck: "Radiation Sickness", sc: 18, decap: "T7", pure: 0.57, win: 0.69 },
  { deck: "The Genome Project", sc: 15, decap: "T7", pure: 0.65, win: 0.66 },
  { deck: "The Replication Crisis", sc: 17, decap: "T7", pure: 0.43, win: 0.59 },
  { deck: "The Exile's Return", sc: 18, decap: "T8", pure: 0.35, win: 0.45 },
  { deck: "Lightning War", sc: 19, decap: "T9", pure: 0.12, win: 0.34 },
];
const columns: Column<Row>[] = [
  { key: "deck", label: "Deck" },
  { key: "sc", label: "Sc", mono: true },
  { key: "decap", label: "decap", mono: true },
  { key: "pure", label: "pure", mono: true, render: (r) => `${(r.pure * 100).toFixed(0)}%` },
  { key: "win", label: "P(WIN)", mono: true, bar: (r) => r.win, render: (r) => `${(r.win * 100).toFixed(0)}%` },
];

export const Default: Story = {
  render: () => <StatTable columns={columns} rows={rows} rowKey={(r) => r.deck} />,
};
