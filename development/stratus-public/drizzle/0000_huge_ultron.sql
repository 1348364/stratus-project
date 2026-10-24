CREATE TABLE `feedback` (
	`id` text PRIMARY KEY NOT NULL,
	`topic` text NOT NULL,
	`message` text NOT NULL,
	`reply` text NOT NULL,
	`created` text NOT NULL,
	`status` text NOT NULL,
	`receipt` text,
	`ip` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `limits` (
	`key` text PRIMARY KEY NOT NULL,
	`count` integer NOT NULL
);
