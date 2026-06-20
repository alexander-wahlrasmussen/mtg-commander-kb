import type { Meta, StoryObj } from "@storybook/react";
import { TabBar } from "./TabBar";

const meta: Meta<typeof TabBar> = { title: "TabBar", component: TabBar };
export default meta;
type Story = StoryObj<typeof TabBar>;

const tabs = [
  { id: "gauntlet", label: "⚔️ Gauntlet" },
  { id: "clocks", label: "⏱️ Clocks / Labs" },
  { id: "locks", label: "🔒 Locks" },
  { id: "championship", label: "🏆 Championship" },
];

export const Default: Story = { args: { tabs, active: "gauntlet", onChange: () => {} } };
export const ChampionshipActive: Story = { args: { tabs, active: "championship", onChange: () => {} } };
