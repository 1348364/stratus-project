ALTER TABLE `feedback` ADD `mail_attempts` integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE `feedback` ADD `mail_first` integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE `feedback` ADD `mail_next` integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE `feedback` ADD `mail_lease` integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE `feedback` ADD `mail_payload` text;--> statement-breakpoint
ALTER TABLE `feedback` ADD `mail_error` text;