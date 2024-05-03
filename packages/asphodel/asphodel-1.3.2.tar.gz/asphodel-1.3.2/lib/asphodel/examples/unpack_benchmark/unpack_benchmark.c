/*
 * Copyright (c) 2019, Suprock Technologies
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
 * SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
 * OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <time.h>

#include <Windows.h>

#include "unpack.h"


static LARGE_INTEGER clock_freq;


static double clock_diff(LARGE_INTEGER *end_time, LARGE_INTEGER *start_time)
{
	if (start_time->QuadPart < end_time->QuadPart)
	{
		LARGE_INTEGER diff;
		diff.QuadPart = end_time->QuadPart - start_time->QuadPart;
		return (double)diff.QuadPart / (double)clock_freq.QuadPart;
	}
	else
	{
		return 0.0;
	}
}

static void test_func(unpack_func_t func, void * unpack_closure, int count, int bits, int is_signed, int offset)
{
	int input_bits = offset + count * bits;
	int input_bytes = (input_bits + 7) / 8;

	volatile uint8_t *input = malloc(input_bytes);
	volatile double* output = malloc(sizeof(double) * count);

	if (input == NULL || output == NULL)
	{
		return;
	}

	for (int i = 0; i < input_bytes; i++)
	{
		input[i] = rand();
	}

	LARGE_INTEGER start;
	QueryPerformanceCounter(&start);

	for (int i = 0; i < 100000; i++)
	{
		func((uint8_t*)input, (double*)output, unpack_closure);
	}

	LARGE_INTEGER end;
	QueryPerformanceCounter(&end);
	double time_spent = clock_diff(&end, &start) * 1e6;

	const char* signed_str = is_signed ? "signed" : "unsigned";
	printf("unpack_%02d_%02dbit_%s_%doff %lf\n", count, bits, signed_str, offset, time_spent);
}

int main(void)
{
	int count;
	int bits;
	int offset;
	int is_signed = 0;

	QueryPerformanceFrequency(&clock_freq);

	for (bits = 1; bits <= 8; bits++)
	{
		for (offset = 0; offset < 1; offset++)
		{
			count = 1;
			while (count <= 8)
			{
				void *unpack_closure;
				unpack_func_t func = find_unpack(count, bits, is_signed, offset, &unpack_closure);
				if (func == NULL)
				{
					break;
				}

				test_func(func, unpack_closure, count, bits, is_signed, offset);

				count += 1;
			}
		}
	}

	return 0;
}
