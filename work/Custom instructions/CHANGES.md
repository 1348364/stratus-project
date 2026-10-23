# Stratus — changes for the next coding pass

Put only the changes you want worked on now under **Pending changes**. `TASK.md` is the complete shader target and remains in force for everything else. A saved file does not start work; tell the coding chat **“Apply the pending changes.”** After implementation and verification, move completed requests to [COMPLETED-CHANGES.md](COMPLETED-CHANGES.md) with the release/evidence reference. If none remain pending, leave **“No pending changes.”** Partial or unverified work stays pending. Studio run actions save the submitted brief as a separate `IN-PROGRESS/<request-id>/CHANGES.md` batch and clear this pending section for your next requests. The coder works on that saved batch; queued work is not completed work.

## Pending changes

- Disallow sheem behind blocks like inside leaf blocks. Current: sheem applies to all surfaces including inside faces/blocks. 

- Block faces that are facing the sun is too reflective, reflecting sunlight too much. 

- When water is set to Vanilla, looking up underwater does not match vanilla underwater style, match it with the vanilla texture options slider. 

- Fix indoor flowing water bug. An image of it can be found in my minecraft screenshots folder. 

- Fix entity shading: entities currently does not have any shade, appily vanilla shading back to the entities

- This shader is soo laggy for no reason (FPS Avg about 25), please research and find ways to fix this, its been a problem for many versions. Oh! I think it might be bc its not using screen space curlling, so like the places the camera can't see won't get renderd. And frame skipping, so when rendering a frame the camera won't wait for the frame to finsh calculating before showing it on screen, it instead does live rendering so what every pixel the GPU outputs gets directly shown on screen, if the frame hasn't been fully renderd then it would just go on to the next frame, making it reach the users fps. When frame skipping is active in high demand areas I should be able to see some pexels not being renderd like starting a render in Blender. 

- Make sure that every new shader you make is inside the game shaderpacks too.

