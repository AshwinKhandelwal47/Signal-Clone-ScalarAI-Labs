import { AVATAR_COLORS, type AvatarColor } from "./constants";
import type { Conversation, User } from "./types";

/** Finds the other participant in a 1:1 direct conversation. */
export function otherMember(conversation: Conversation, meId: number): User | undefined {
  if (conversation.type !== "direct") return undefined;
  return conversation.members.find((m) => m.user.id !== meId)?.user;
}

/** Computes display title: group name for groups, recipient display name for direct chats. */
export function conversationTitle(conversation: Conversation, meId: number): string {
  if (conversation.type === "group") return conversation.name ?? "Group";
  return otherMember(conversation, meId)?.display_name ?? "Unknown";
}

/** Groups have no stored colour, so derive a stable one from the id. */
export function conversationColor(conversation: Conversation, meId: number): string {
  if (conversation.type === "direct") return otherMember(conversation, meId)?.avatar_color ?? "A210";
  const keys = Object.keys(AVATAR_COLORS) as AvatarColor[];
  return keys[conversation.id % keys.length];
}

/** Returns the latest timestamp between last message and creation time for ordering. */
export function lastActivity(conversation: Conversation): string {
  return conversation.last_message?.created_at ?? conversation.created_at;
}

/** Sorts a list of conversations in descending order of newest activity. */
export function sortByActivity(conversations: Conversation[]): Conversation[] {
  return [...conversations].sort((a, b) => Date.parse(lastActivity(b)) - Date.parse(lastActivity(a)));
}

/** Evaluates whether a conversation matches a search filter by title or member name/username. */
export function matchesSearch(conversation: Conversation, query: string, meId: number): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  if (conversationTitle(conversation, meId).toLowerCase().includes(q)) return true;
  return conversation.members.some(
    (m) =>
      m.user.id !== meId && (m.user.display_name.toLowerCase().includes(q) || m.user.username?.includes(q)),
  );
}


/** Contact search: matches name, username (with or without "@") or phone digits. */
export function contactMatches(user: User, query: string): boolean {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return (
    user.display_name.toLowerCase().includes(q) ||
    !!user.username?.includes(q.replace(/^@/, "")) ||
    !!user.phone_number?.includes(q.replace(/[\s()-]/g, ""))
  );
}
