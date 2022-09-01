#pragma once

#include <napi.h>
#include <string>
#include "DWrap.h"


Napi::Object InitAll(Napi::Env env, Napi::Object exports) {
	return DWrap::Init(env, exports);
}



NODE_API_MODULE(NODE_GYP_MODULE_NAME, InitAll)






