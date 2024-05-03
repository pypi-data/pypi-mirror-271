set(UNPACK_BENCHMARK_SOURCES unpack_benchmark.c)

add_executable(unpack_benchmark ${UNPACK_BENCHMARK_SOURCES})

target_link_libraries(unpack_benchmark asphodel)

if(MSVC)
	target_compile_definitions(unpack_benchmark PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

install(TARGETS unpack_benchmark RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT bin)
