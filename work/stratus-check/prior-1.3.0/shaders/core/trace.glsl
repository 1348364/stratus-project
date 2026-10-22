#ifndef STRATUS_TRACE_INCLUDED
#define STRATUS_TRACE_INCLUDED
uniform sampler2D depthtex1;
uniform sampler2D colortex4;

float screenDepthError(vec3 rayPoint, vec2 coordinate) {
    float sampledDepth = texture(depthtex1, coordinate).r;
    if (sampledDepth >= 0.999999) return -100000.0;
    return positionFromDepth(coordinate, sampledDepth).z - rayPoint.z;
}
vec4 sceneryReflection(vec3 viewOrigin, vec3 viewDirection) {
#if REFLECTION_MODE == 0
    return vec4(0.0);
#else
    float distanceLimit = min(REFLECT_RANGE, max(16.0, far));
    if (viewDirection.z > 0.00001)
        distanceLimit = min(distanceLimit, max(0.0, (-0.15 - viewOrigin.z) / viewDirection.z));
    if (distanceLimit < 0.1) return vec4(0.0);
    vec3 rayEnd = viewOrigin + viewDirection * distanceLimit;
    vec4 clipBegin = gbufferProjection * vec4(viewOrigin, 1.0);
    vec4 clipEnd = gbufferProjection * vec4(rayEnd, 1.0);
    float reciprocalBegin = 1.0 / max(clipBegin.w, 0.00001);
    float reciprocalEnd = 1.0 / max(clipEnd.w, 0.00001);
    vec2 screenBegin = clipBegin.xy * reciprocalBegin * 0.5 + 0.5;
    vec2 screenEnd = clipEnd.xy * reciprocalEnd * 0.5 + 0.5;
    vec3 projectiveBegin = viewOrigin * reciprocalBegin;
    vec3 projectiveEnd = rayEnd * reciprocalEnd;
#if REFLECTION_MODE == 2
    const int count = 28;
    const int bisections = 5;
#else
    const int count = 16;
    const int bisections = 4;
#endif
    float previousFraction = 0.0;
    float previousError = -1.0;
    for (int sampleIndex = 1; sampleIndex <= count; sampleIndex++) {
        float fraction = float(sampleIndex) / float(count);
        vec2 screen = mix(screenBegin, screenEnd, fraction);
        if (min(screen.x, screen.y) < 0.001 || max(screen.x, screen.y) > 0.999) break;
        float reciprocal = mix(reciprocalBegin, reciprocalEnd, fraction);
        vec3 rayPoint = mix(projectiveBegin, projectiveEnd, fraction) / reciprocal;
        float error = screenDepthError(rayPoint, screen);
        if (error >= 0.0 && previousError < 0.0) {
            float left = previousFraction, right = fraction;
            for (int refinement = 0; refinement < bisections; refinement++) {
                float middle = (left + right) * 0.5;
                vec2 middleScreen = mix(screenBegin, screenEnd, middle);
                vec3 middlePoint = mix(projectiveBegin, projectiveEnd, middle)
                                 / mix(reciprocalBegin, reciprocalEnd, middle);
                if (screenDepthError(middlePoint, middleScreen) >= 0.0) right = middle;
                else left = middle;
            }
            vec2 hitScreen = mix(screenBegin, screenEnd, right);
            vec3 hitPoint = mix(projectiveBegin, projectiveEnd, right)
                          / mix(reciprocalBegin, reciprocalEnd, right);
            float missDistance = abs(screenDepthError(hitPoint, hitScreen));
            float tolerance = 0.22 + abs(hitPoint.z) * 0.009;
            vec2 border = min(hitScreen, 1.0 - hitScreen);
            float confidence = 1.0 - smoothstep(tolerance * 0.35, tolerance, missDistance);
            confidence *= smoothstep(0.0, 0.075, min(border.x, border.y));
            confidence *= smoothstep(0.35, 1.4, -hitPoint.z);
            confidence *= 1.0 - smoothstep(distanceLimit * 0.67, distanceLimit, length(hitPoint - viewOrigin));
            vec4 centre = texture(colortex4, hitScreen);
            confidence *= centre.a;
            vec2 texel = vec2(0.85, 0.45) / viewportSize();
            vec3 softened = centre.rgb * 0.60
                          + texture(colortex4, hitScreen + texel).rgb * 0.20
                          + texture(colortex4, hitScreen - texel).rgb * 0.20;
            return vec4(softened, clamp(confidence, 0.0, 1.0));
        }
        previousFraction = fraction;
        previousError = error;
    }
    return vec4(0.0);
#endif
}
#endif
