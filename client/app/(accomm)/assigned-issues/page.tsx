"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "react-toastify";

type Issue = {
  id: string;
  title: string;
  description: string;
  status: "reported" | "in_progress" | "resolved";
  priority: "low" | "medium" | "high";
  apartment_unit: string;
  reported_by: string;
  assigned_to: string;
};

const statusStyles: Record<Issue["status"], string> = {
  reported: "bg-slate-100 text-slate-700",
  in_progress: "bg-blue-100 text-blue-700",
  resolved: "bg-green-100 text-green-700",
};

const priorityStyles: Record<Issue["priority"], string> = {
  low: "bg-slate-100 text-slate-700",
  medium: "bg-amber-100 text-amber-700",
  high: "bg-red-100 text-red-700",
};

export default function AssignedIssuesPage() {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/v1/issues/assigned/`, {
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load assigned issues");
        return res.json();
      })
      .then((data) => {
        setIssues(data.data.results);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Could not load assigned issues");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="p-6 text-baby_richBlack">Loading assigned issues...</p>;
  }

  return (
    <div className="p-6">
      <h1 className="h1-bold mb-6 text-baby_richBlack">Assigned Issues</h1>

      {issues.length === 0 ? (
        <p className="text-baby_richBlack">
          You have no issues assigned to you right now.
        </p>
      ) : (
        <div className="flex flex-col gap-4">
        {issues.map((issue) => (
  <Link
    key={issue.id}
    href={`/issue/update-issue/${issue.id}`}
    className="bg-baby_rich light-border rounded-lg border p-5 shadow-platinum block transition hover:shadow-lg"
  >
    <div className="flex items-center justify-between mb-2">
      <h2 className="h3-bold text-baby_richBlack">{issue.title}</h2>
      <span
        className={`rounded-full px-3 py-1 text-xs font-semibold ${priorityStyles[issue.priority]}`}
      >
        {issue.priority}
      </span>
    </div>

    <p className="text-baby_richBlack line-clamp-2">
      {issue.description}
    </p>

    <div className="mt-3 flex flex-wrap items-center gap-4 text-sm text-baby_richBlack">
      <span>Apartment: {issue.apartment_unit}</span>
      <span>Reported by: {issue.reported_by}</span>
      <span
        className={`rounded-full px-2 py-0.5 font-medium ${statusStyles[issue.status]}`}
      >
        {issue.status.replace("_", " ")}
      </span>
    </div>
  </Link>
))}
        </div>
      )}
    </div>
  );
}