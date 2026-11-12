'use client';

import { useUserFiltersStore, usePostFiltersStore } from '@/lib/stores/filters-store';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '../ui/pagination';

interface PaginationSectionProps {
  totalPages: number;
  entityType: 'user' | 'post';
}

const PaginationSection = ({ totalPages, entityType }: PaginationSectionProps) => {
  const userPage = useUserFiltersStore((s) => s.page);
  const setUserPage = useUserFiltersStore((s) => s.setCurrentPage);
  const postPage = usePostFiltersStore((s) => s.page);
  const setPostPage = usePostFiltersStore((s) => s.setCurrentPage);

  const currentPage = entityType === 'user' ? userPage : postPage;
  const setCurrentPage = entityType === 'user' ? setUserPage : setPostPage;

  const handlePreviousClick = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };
  const handleNextClick = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  return (
    <Pagination className="bg-platinum dark:bg-eerieBlack dark:text-platinum mt-4 rounded-full">
      <PaginationContent>
        <PaginationItem className="cursor-pointer">
          <PaginationPrevious onClick={handlePreviousClick} />
        </PaginationItem>
        <PaginationItem className="h3-semibold font-robotoSlab dark:text-veryBlack inline-flex items-center rounded-md border border-transparent bg-lime-500">
          {currentPage}
        </PaginationItem>
        <PaginationItem className="cursor-pointer">
          <PaginationNext onClick={handleNextClick} />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

export default PaginationSection;
