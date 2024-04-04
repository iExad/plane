import { observer } from "mobx-react-lite";
// components
import { EmptyState } from "@/components/empty-state";
// constants
import { EMPTY_STATE_DETAILS } from "@/constants/empty-state";
// hooks
import { useApplication } from "@/hooks/store";

// assets

export const ProfileViewEmptyState: React.FC = observer(() => {
  // store hooks
  const {
    router: { profileViewId },
  } = useApplication();

  if (!profileViewId) return null;

  const emptyStateType = `profile-${profileViewId}`;

  return <EmptyState type={emptyStateType as keyof typeof EMPTY_STATE_DETAILS} size="sm" />;
});
