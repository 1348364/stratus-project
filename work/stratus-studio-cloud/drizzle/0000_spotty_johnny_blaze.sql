CREATE TABLE `documents` (
	`id` text PRIMARY KEY NOT NULL,
	`text` text NOT NULL,
	`revision` text NOT NULL,
	`modified` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `history` (
	`id` text PRIMARY KEY NOT NULL,
	`document` text NOT NULL,
	`text` text NOT NULL,
	`revision` text NOT NULL,
	`modified` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `jobs` (
	`id` text PRIMARY KEY NOT NULL,
	`operation` text NOT NULL,
	`instructions` text NOT NULL,
	`revisions` text NOT NULL,
	`status` text NOT NULL,
	`detail` text NOT NULL,
	`queueId` text,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `metadata` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL
);
