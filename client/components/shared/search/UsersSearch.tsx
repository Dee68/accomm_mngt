'use client';

import { Input } from '@/components/ui/input';
import { useUserFiltersStore } from '@/lib/stores/filters-store';
import Image from 'next/image';
import React from 'react';

const UsersSearch = () => {
  const searchTerm = useUserFiltersStore((s) => s.searchTerm);
  const setSearchTerm = useUserFiltersStore((s) => s.setSearchTerm);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  return (
    <div className="flex min-h-[56px] bg-gray dark:bg-eerieBlack mb-3 w-full grow rounded-full">
      <Image
        src="/assets/icons/search.svg"
        alt="Search"
        width={24}
        height={24}
        className="mx-3"
      />
      <Input
        placeholder="Search by username, first or last name"
        type="search"
        value={searchTerm}
        onChange={handleInputChange}
        className="search-text no-focus dark:text-babyPowder border-none bg-transparent shadow-none outline-none"
      />
    </div>
  );
};

export default UsersSearch;
