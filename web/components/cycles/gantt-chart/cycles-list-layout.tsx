import { FC } from "react";
import { useRouter } from "next/router";
import { observer } from "mobx-react-lite";
import { KeyedMutator } from "swr";
// hooks
import { useUser } from "hooks/store";
// services
import { CycleService } from "services/cycle.service";
// components
import { GanttChartRoot, IBlockUpdateData, CycleGanttSidebar } from "components/gantt-chart";
import { CycleGanttBlock } from "components/cycles";
// types
import { ICycle } from "types";
// constants
import { EUserWorkspaceRoles } from "constants/workspace";

type Props = {
  workspaceSlug: string;
  cycles: ICycle[];
  mutateCycles?: KeyedMutator<ICycle[]>;
};

// services
const cycleService = new CycleService();

export const CyclesListGanttChartView: FC<Props> = observer((props) => {
  const { cycles, mutateCycles } = props;
  // router
  const router = useRouter();
  const { workspaceSlug } = router.query;
  // store hooks
  const {
    membership: { currentProjectRole },
  } = useUser();

  const handleCycleUpdate = (cycle: ICycle, payload: IBlockUpdateData) => {
    if (!workspaceSlug) return;
    mutateCycles &&
      mutateCycles((prevData: any) => {
        if (!prevData) return prevData;

        const newList = prevData.map((p: any) => ({
          ...p,
          ...(p.id === cycle.id
            ? {
                start_date: payload.start_date ? payload.start_date : p.start_date,
                target_date: payload.target_date ? payload.target_date : p.end_date,
                sort_order: payload.sort_order ? payload.sort_order.newSortOrder : p.sort_order,
              }
            : {}),
        }));

        if (payload.sort_order) {
          const removedElement = newList.splice(payload.sort_order.sourceIndex, 1)[0];
          newList.splice(payload.sort_order.destinationIndex, 0, removedElement);
        }

        return newList;
      }, false);

    const newPayload: any = { ...payload };

    if (newPayload.sort_order && payload.sort_order) newPayload.sort_order = payload.sort_order.newSortOrder;

    cycleService.patchCycle(workspaceSlug.toString(), cycle.project, cycle.id, newPayload);
  };

  const blockFormat = (blocks: ICycle[]) =>
    blocks && blocks.length > 0
      ? blocks
          .filter((b) => b.start_date && b.end_date && new Date(b.start_date) <= new Date(b.end_date))
          .map((block) => ({
            data: block,
            id: block.id,
            sort_order: block.sort_order,
            start_date: new Date(block.start_date ?? ""),
            target_date: new Date(block.end_date ?? ""),
          }))
      : [];

  const isAllowed =
    currentProjectRole && [EUserWorkspaceRoles.ADMIN, EUserWorkspaceRoles.MEMBER].includes(currentProjectRole);

  return (
    <div className="h-full w-full overflow-y-auto">
      <GanttChartRoot
        title="Cycles"
        loaderTitle="Cycles"
        blocks={cycles ? blockFormat(cycles) : null}
        blockUpdateHandler={(block, payload) => handleCycleUpdate(block, payload)}
        sidebarToRender={(props) => <CycleGanttSidebar {...props} />}
        blockToRender={(data: ICycle) => <CycleGanttBlock data={data} />}
        enableBlockLeftResize={false}
        enableBlockRightResize={false}
        enableBlockMove={false}
        enableReorder={isAllowed}
      />
    </div>
  );
});
